import requests
import json

# Base URL of the FastAPI application
BASE_URL = "http://127.0.0.1:8000"

# Function to test GET requests
def test_get(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    print(f"GET {url} -> Status: {response.status_code}")
    print(response.json())

# Function to test POST requests
def test_post(endpoint, data):
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"POST {url} -> Status: {response.status_code}")
    print(response.json())
    return response.json()

# Function to test PUT requests
def test_put(endpoint, data):
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, data=json.dumps(data), headers=headers)
    print(f"PUT {url} -> Status: {response.status_code}")
    print(response.json())

# Function to test DELETE requests
def test_delete(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.delete(url)
    print(f"DELETE {url} -> Status: {response.status_code}")
    print(response.json())

# Test GET all customers, products, sales, stores
test_get("customers")
test_get("products")
test_get("sales")
test_get("stores")

# Test POST - Creating new records
new_customer = {
    "CustomerKey": 9999,
    "Gender": "Male",
    "Name": "Test Customer",
    "City": "Test City",
    "StateCode": "TC",
    "State": "Test State",
    "ZipCode": "12345",
    "Country": "Testland",
    "Continent": "Test Continent",
    "Birthday": "1990-01-01"
}
test_post("customers", new_customer)

new_product = {
    "ProductKey": 9999,
    "ProductName": "Test Product",
    "Brand": "Test Brand",
    "Color": "Red",
    "UnitCostUSD": 10.5,
    "UnitPriceUSD": 15.0,
    "SubcategoryKey": 1,
    "Subcategory": "Test Subcategory",
    "CategoryKey": 1,
    "Category": "Test Category"
}
test_post("products", new_product)

new_store = {
    "StoreKey": 9999,
    "Country": "Testland",
    "State": "Test State",
    "SquareMeters": 100.5,
    "OpenDate": "2020-01-01"
}
test_post("stores", new_store)

new_sale = {
    "OrderNumber": 9999,
    "LineItem": 1,
    "OrderDate": "2023-01-01",
    "DeliveryDate": "2023-01-10",
    "CustomerKey": 9999,
    "StoreKey": 9999,
    "ProductKey": 9999,
    "Quantity": 5,
    "CurrencyCode": "USD"
}
test_post("sales", new_sale)

# Test PUT - Updating records
updated_customer = {"Name": "Updated Customer", "City": "Updated City"}
test_put("customers/9999", updated_customer)

updated_product = {"UnitPriceUSD": 12.99}
test_put("products/9999", updated_product)

# Test DELETE - Removing records
test_delete("customers/9999")
test_delete("products/9999")
test_delete("stores/9999")
test_delete("sales/9999/1")
