from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query, Path
from config.env import get_session
from db.models import Sales
from sqlmodel import Session, select

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/sales",
    tags=["sales"],
    responses={
        status.HTTP_201_CREATED: {"description": "Sales record successfully added"},
        status.HTTP_404_NOT_FOUND: {"description": "Sales record not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)

# ------ CRUD Operations ------

# Create a new sales record
@router.post("/", response_model=Sales, summary="Insert a sales record with the provided details into the sales table")
def create_sales_record(sales: Sales, session: SessionDep):
    try:
        session.add(sales)
        session.commit()
        session.refresh(sales)
        return sales
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Exception raised: {e}")


# Get a list of sales records with pagination
@router.get("/", response_model=dict, summary="List sales records information from offset+1 to the desired limit")
def read_sales_records(
    session: SessionDep,
    response: Response,
    offset: Annotated[int, Query(description="Number of records to skip")] = 0,
    limit: Annotated[int, Query(le=10, description="Maximum number of records to retrieve")] = 5,
):
    query = select(Sales).offset(offset).limit(limit)
    results = session.exec(query)
    sales_records = results.all()
    
    return {"data": sales_records, "count": len(sales_records)}


# Get a specific sales record by OrderNumber and LineItem
@router.get("/{order_number}/{line_item}", response_model=Sales, summary="Get a specific sales record's information using OrderNumber and LineItem")
def read_sales_record_by_id(
    session: SessionDep,
    order_number: Annotated[int, Path(description="Order number of the sales record to retrieve")],
    line_item: Annotated[int, Path(description="Line item of the sales record to retrieve")],
    response: Response,
):
    response.headers["Cache-Control"] = "no-cache"

    sales_record = session.get(Sales, (order_number, line_item))
    if not sales_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales record with OrderNumber {order_number} and LineItem {line_item} not found")
    
    return sales_record


# Full update of a sales record
@router.put("/{order_number}/{line_item}", response_model=Sales, status_code=status.HTTP_200_OK)
def update_sales_record(
    session: SessionDep,
    order_number: Annotated[int, Path(description="Order number of the sales record to update")],
    line_item: Annotated[int, Path(description="Line item of the sales record to update")],
    sales: Sales,
):
    sales_record_db = session.get(Sales, (order_number, line_item))
    if not sales_record_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales record with OrderNumber {order_number} and LineItem {line_item} not found")
    
    sales_data = sales.dict()
    for key, value in sales_data.items():
        setattr(sales_record_db, key, value)
    
    session.add(sales_record_db)
    session.commit()
    session.refresh(sales_record_db)
    return sales_record_db


# Partial update of a sales record
@router.patch("/{order_number}/{line_item}", response_model=Sales, status_code=status.HTTP_200_OK)
def partially_update_sales_record(
    session: SessionDep,
    order_number: Annotated[int, Path(description="Order number of the sales record to update")],
    line_item: Annotated[int, Path(description="Line item of the sales record to update")],
    sales: Sales,
):
    sales_record_db = session.get(Sales, (order_number, line_item))
    if not sales_record_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales record with OrderNumber {order_number} and LineItem {line_item} not found")
    
    sales_data = sales.dict(exclude_unset=True)
    for key, value in sales_data.items():
        setattr(sales_record_db, key, value)
    
    session.add(sales_record_db)
    session.commit()
    session.refresh(sales_record_db)
    return sales_record_db


# Delete a sales record
@router.delete("/{order_number}/{line_item}", summary="Delete a specific sales record using OrderNumber and LineItem", status_code=status.HTTP_200_OK)
def delete_sales_record(
    session: SessionDep,
    order_number: Annotated[int, Path(description="Order number of the sales record to remove")],
    line_item: Annotated[int, Path(description="Line item of the sales record to remove")],
):
    sales_record = session.get(Sales, (order_number, line_item))
    if not sales_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales record with OrderNumber {order_number} and LineItem {line_item} not found")
    
    session.delete(sales_record)
    session.commit()
    return {status.HTTP_200_OK: f"Sales record with OrderNumber {order_number} and LineItem {line_item} successfully deleted"}