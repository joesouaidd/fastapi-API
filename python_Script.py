# Python script that builds the SQLite Database
import sqlite3
import pandas as pd
import os

# Ensure the ./db directory exists
#os.makedirs('./db', exist_ok=True)

# Define the database name with the path to the ./db folder
db_name = "./db/retailer_database.db"

# Establish the SQLite connection
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Function to execute SQL DDL script
def execute_ddl_script(file_path):
    print(f"Executing DDL script: {file_path}")
    with open(file_path, 'r') as ddl_file:
        ddl_script = ddl_file.read()
    cursor.executescript(ddl_script)
    conn.commit()

# Call the DDL script to create tables
ddl_file_path = "create_tables.sql"  # Path to your DDL script
execute_ddl_script(ddl_file_path)

# Define function to load CSV into a table
def load_csv_to_table(csv_file, table_name):
    print(f"Loading data into {table_name} from {csv_file}")
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        print(f"Encoding error with {csv_file}. Retrying with ISO-8859-1 encoding.")
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    df.to_sql(table_name, conn, if_exists='append', index=False)

# Load CSV data into corresponding tables
csv_files = {
    "Customers": "Data/Customers.csv",
    "DataDictionary": "Data/Data_Dictionary.csv",
    "ExchangeRates": "Data/Exchange_Rates.csv",
    "Products": "Data/Products.csv",
    "Sales": "Data/Sales.csv",
    "Stores": "Data/Stores.csv"
}

for table, file in csv_files.items():
    load_csv_to_table(file, table)

# Close the connection
conn.close()
print(f"Database {db_name} created and populated successfully.")
