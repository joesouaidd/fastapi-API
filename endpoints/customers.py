from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query, Path
from config.env import get_session
from db.models import Customers
from sqlmodel import Session, select

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={
        status.HTTP_201_CREATED: {"description": "Customers successfully added"},
        status.HTTP_404_NOT_FOUND: {"description": "Customers not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)

# ------ CRUD Operations ------

# Create a new customer
@router.post("/", response_model=Customers, summary="Insert a customer with the provided details into the customer table")
def create_customer(customer: Customers, session: SessionDep):
    try:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Exception raised: {e}")


# Get a list of Customers with pagination
@router.get("/", response_model=dict, summary="List customers information from offset+1 to the desired limit")
def read_customers(
    session: SessionDep,
    response: Response,
    offset: Annotated[int, Query(description="Number of records to skip")] = 0,
    limit: Annotated[int, Query(le=10, description="Maximum number of records to retrieve")] = 5,
):
    query = select(Customers).offset(offset).limit(limit)
    results = session.exec(query)
    customers = results.all()
    
    return {"data": customers, "count": len(customers)}


# Get a specific customer by ID
@router.get("/{customer_id}", response_model=Customers, summary="Get a specific customer's information using their ID")
def read_customer_by_id(
    session: SessionDep,
    customer_id: Annotated[int, Path(description="ID of the customer to retrieve")],
    response: Response,
):
    response.headers["Cache-Control"] = "no-cache"

    customer = session.get(Customers, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {customer_id} not found")
    
    return customer


# Full update of a customer
@router.put("/{customer_id}", response_model=Customers, status_code=status.HTTP_200_OK)
def update_customer(
    session: SessionDep,
    customer_id: Annotated[int, Path(description="ID of the customer to update")],
    customer: Customers,
):
    customer_db = session.get(Customers, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {customer_id} not found")
    
    customer_data = customer.dict()
    for key, value in customer_data.items():
        setattr(customer_db, key, value)
    
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


# Partial update of a customer
@router.patch("/{customer_id}", response_model=Customers, status_code=status.HTTP_200_OK)
def partially_update_customer(
    session: SessionDep,
    customer_id: Annotated[int, Path(description="ID of the customer to update")],
    customer: Customers,
):
    customer_db = session.get(Customers, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {customer_id} not found")
    
    customer_data = customer.dict(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(customer_db, key, value)
    
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


# Delete a customer
@router.delete("/{customer_id}", summary="Delete a specific customer using their ID", status_code=status.HTTP_200_OK)
def delete_customer(
    session: SessionDep,
    customer_id: Annotated[int, Path(description="ID of the customer to remove")],
):
    customer = session.get(Customers, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {customer_id} not found")
    
    session.delete(customer)
    session.commit()
    return {status.HTTP_200_OK: f"Customer {customer_id} successfully deleted"}
