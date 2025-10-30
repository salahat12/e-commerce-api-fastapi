import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="E-Commerce API")

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_ROOT_PASSWORD",
    "database": "fastapi_db"
}

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/products/")
def create_product(product: Product):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, in_stock) VALUES (%s, %s, %s)",
        (product.name, product.price, product.in_stock)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Product created"}

@app.get("/products/")
def get_products():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
