from typing import Optional
from sqlmodel import Field, PrimaryKeyConstraint, SQLModel

class Customers(SQLModel, table=True):
    CustomerKey: Optional[int] = Field(default=None, primary_key=True)
    Gender: Optional[str] = None
    Name: str
    City: Optional[str] = None
    StateCode: Optional[str] = None
    State: Optional[str] = None
    ZipCode: Optional[str] = None
    Country: Optional[str] = None
    Continent: Optional[str] = None
    Birthday: Optional[str] = None


class Products(SQLModel, table=True):
    ProductKey: Optional[int] = Field(default=None, primary_key=True)
    ProductName: str
    Brand: Optional[str] = None
    Color: Optional[str] = None
    UnitCostUSD: Optional[float] = None
    UnitPriceUSD: Optional[float] = None
    SubcategoryKey: Optional[int] = None
    Subcategory: Optional[str] = None
    CategoryKey: Optional[int] = None
    Category: Optional[str] = None

class DataDictionary(SQLModel, table=True):
    Table_Source: Optional[str] = None
    Field: Optional[str] = None
    Description: Optional[str] = None
    __table_args__ = (
        PrimaryKeyConstraint('Table_Source', 'Field'),
    )


class ExchangeRates(SQLModel, table=True):
        Date: str
        Currency: str
        Exchange: float
        __table_args__ = (
            PrimaryKeyConstraint('Date', 'Currency'),
        )


class Sales(SQLModel, table=True):
        OrderNumber: int
        LineItem: int
        OrderDate: Optional[str] = None
        DeliveryDate: Optional[str] = None
        CustomerKey: int
        StoreKey: int
        ProductKey: int
        Quantity: Optional[int] = None
        CurrencyCode: Optional[str] = None
        __table_args__ = (
            PrimaryKeyConstraint('OrderNumber', 'LineItem'),
        )


class Stores(SQLModel, table=True):
        StoreKey: Optional[int] = Field(default=None, primary_key=True)
        Country: Optional[str] = None
        State: Optional[str] = None
        SquareMeters: Optional[float] = None
        OpenDate: Optional[str] = None