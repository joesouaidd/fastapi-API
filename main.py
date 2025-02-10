from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from endpoints import customers, products, stores,sales

description = """
This API helps interact with the  Global Electronics Retailer database.

It allows to:

👉 **List all Customers, Products, Sales and Stores**

👉 **Add new Customer, Product or Store**

👉 **Add new Sale**

👉 **...**

Further Informations are below 👇
"""

app = FastAPI(
    title=" Global Electronics Retailer Management System API",
    description=description,
    summary="🎯  Global Electronics Retailer Management System API to interact with the databases",
    version="0.0.1",
    terms_of_service="tos",
    contact= {"name": "FD",
              "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
              "email": "fd@fakeemail.com"},
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

templates = Jinja2Templates(directory="templates")

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(stores.router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})