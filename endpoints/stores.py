from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query, Path
from config.env import get_session
from db.models import Stores
from sqlmodel import Session, select

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    responses={
        status.HTTP_201_CREATED: {"description": "Store successfully added"},
        status.HTTP_404_NOT_FOUND: {"description": "Store not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)

# ------ CRUD Operations ------

# Create a new store
@router.post("/", response_model=Stores, summary="Insert a store with the provided details into the store table")
def create_store(store: Stores, session: SessionDep):
    try:
        session.add(store)
        session.commit()
        session.refresh(store)
        return store
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Exception raised: {e}")


# Get a list of Stores with pagination
@router.get("/", response_model=dict, summary="List stores information from offset+1 to the desired limit")
def read_stores(
    session: SessionDep,
    response: Response,
    offset: Annotated[int, Query(description="Number of records to skip")] = 0,
    limit: Annotated[int, Query(le=10, description="Maximum number of records to retrieve")] = 5,
):
    query = select(Stores).offset(offset).limit(limit)
    results = session.exec(query)
    stores = results.all()
    
    return {"data": stores, "count": len(stores)}


# Get a specific store by ID
@router.get("/{store_id}", response_model=Stores, summary="Get a specific store's information using their ID")
def read_store_by_id(
    session: SessionDep,
    store_id: Annotated[int, Path(description="ID of the store to retrieve")],
    response: Response,
):
    response.headers["Cache-Control"] = "no-cache"

    store = session.get(Stores, store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Store with ID {store_id} not found")
    
    return store


# Full update of a store
@router.put("/{store_id}", response_model=Stores, status_code=status.HTTP_200_OK)
def update_store(
    session: SessionDep,
    store_id: Annotated[int, Path(description="ID of the store to update")],
    store: Stores,
):
    store_db = session.get(Stores, store_id)
    if not store_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Store with ID {store_id} not found")
    
    store_data = store.dict()
    for key, value in store_data.items():
        setattr(store_db, key, value)
    
    session.add(store_db)
    session.commit()
    session.refresh(store_db)
    return store_db


# Partial update of a store
@router.patch("/{store_id}", response_model=Stores, status_code=status.HTTP_200_OK)
def partially_update_store(
    session: SessionDep,
    store_id: Annotated[int, Path(description="ID of the store to update")],
    store: Stores,
):
    store_db = session.get(Stores, store_id)
    if not store_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Store with ID {store_id} not found")
    
    store_data = store.dict(exclude_unset=True)
    for key, value in store_data.items():
        setattr(store_db, key, value)
    
    session.add(store_db)
    session.commit()
    session.refresh(store_db)
    return store_db


# Delete a store
@router.delete("/{store_id}", summary="Delete a specific store using their ID", status_code=status.HTTP_200_OK)
def delete_store(
    session: SessionDep,
    store_id: Annotated[int, Path(description="ID of the store to remove")],
):
    store = session.get(Stores, store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Store with ID {store_id} not found")
    
    session.delete(store)
    session.commit()
    return {status.HTTP_200_OK: f"Store {store_id} successfully deleted"}