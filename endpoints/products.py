from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query, Path
from config.env import get_session
from db.models import Products
from sqlmodel import Session, select

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={
        status.HTTP_201_CREATED: {"description": "Product successfully added"},
        status.HTTP_404_NOT_FOUND: {"description": "Product not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
git 
# ------ CRUD Operations ------

# Create a new product
@router.post("/", response_model=Products, summary="Insert a product with the provided details into the product table")
def create_product(product: Products, session: SessionDep):
    try:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Exception raised: {e}")


# Get a list of Products with pagination
@router.get("/", response_model=dict, summary="List products information from offset+1 to the desired limit")
def read_products(
    session: SessionDep,
    response: Response,
    offset: Annotated[int, Query(description="Number of records to skip")] = 0,
    limit: Annotated[int, Query(le=10, description="Maximum number of records to retrieve")] = 5,
):
    query = select(Products).offset(offset).limit(limit)
    results = session.exec(query)
    products = results.all()
    
    return {"data": products, "count": len(products)}


# Get a specific product by ID
@router.get("/{product_id}", response_model=Products, summary="Get a specific product's information using their ID")
def read_product_by_id(
    session: SessionDep,
    product_id: Annotated[int, Path(description="ID of the product to retrieve")],
    response: Response,
):
    response.headers["Cache-Control"] = "no-cache"

    product = session.get(Products, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} not found")
    
    return product


# Full update of a product
@router.put("/{product_id}", response_model=Products, status_code=status.HTTP_200_OK)
def update_product(
    session: SessionDep,
    product_id: Annotated[int, Path(description="ID of the product to update")],
    product: Products,
):
    product_db = session.get(Products, product_id)
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} not found")
    
    product_data = product.dict()
    for key, value in product_data.items():
        setattr(product_db, key, value)
    
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db


# Partial update of a product
@router.patch("/{product_id}", response_model=Products, status_code=status.HTTP_200_OK)
def partially_update_product(
    session: SessionDep,
    product_id: Annotated[int, Path(description="ID of the product to update")],
    product: Products,
):
    product_db = session.get(Products, product_id)
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} not found")
    
    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product_db, key, value)
    
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db


# Delete a product
@router.delete("/{product_id}", summary="Delete a specific product using their ID", status_code=status.HTTP_200_OK)
def delete_product(
    session: SessionDep,
    product_id: Annotated[int, Path(description="ID of the product to remove")],
):
    product = session.get(Products, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} not found")
    
    session.delete(product)
    session.commit()
    return {status.HTTP_200_OK: f"Product {product_id} successfully deleted"}