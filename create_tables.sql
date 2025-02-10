-- SQL DDL script to build the tables

CREATE TABLE IF NOT EXISTS Customers (
    CustomerKey INTEGER PRIMARY KEY,
    Gender TEXT,
    Name TEXT NOT NULL,
    City TEXT,
    StateCode TEXT,
    State TEXT,
    ZipCode TEXT,
    Country TEXT,
    Continent TEXT,
    Birthday TEXT
);

CREATE TABLE IF NOT EXISTS DataDictionary (
    Table_Source TEXT,
    Field TEXT,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS ExchangeRates (
    Date TEXT NOT NULL,
    Currency TEXT NOT NULL,
    Exchange DECIMAL(10, 6)  NOT NULL,
    PRIMARY KEY (Date, Currency)
);

CREATE TABLE IF NOT EXISTS Products (
    ProductKey INTEGER PRIMARY KEY,
    ProductName TEXT NOT NULL,
    Brand TEXT,
    Color TEXT,
    UnitCostUSD DECIMAL(10, 6) ,
    UnitPriceUSD DECIMAL(10, 6) ,
    SubcategoryKey INTEGER,
    Subcategory TEXT,
    CategoryKey INTEGER,
    Category TEXT
);

CREATE TABLE IF NOT EXISTS Sales (
    OrderNumber INTEGER,
    LineItem INTEGER,
    OrderDate TEXT,
    DeliveryDate TEXT,
    CustomerKey INTEGER NOT NULL,
    StoreKey INTEGER NOT NULL,
    ProductKey INTEGER NOT NULL,
    Quantity INTEGER,
    CurrencyCode TEXT,
    PRIMARY KEY (OrderNumber, LineItem),
    FOREIGN KEY (CustomerKey) REFERENCES Customers(CustomerKey),
    FOREIGN KEY (StoreKey) REFERENCES Stores(StoreKey),
    FOREIGN KEY (ProductKey) REFERENCES Products(ProductKey)
);

CREATE TABLE IF NOT EXISTS Stores (
    StoreKey INTEGER PRIMARY KEY,
    Country TEXT,
    State TEXT,
    SquareMeters REAL,
    OpenDate TEXT
);
