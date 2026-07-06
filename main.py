'''
import fastapi

app 

get >> return date >> path paramter 
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

con = sqlite3.connect('newdatabase.db', check_same_thread=False)
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS products
            (id INTEGER PRIMARY KEY AUTOINCREMENT,  
            name TEXT ,
            price REAL)''')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # في الإنتاج تقدر تحدد رابط الـ Front-end بتاعك بالظبط
    allow_credentials=True,
    allow_methods=["*"], # السماح بـ GET, POST, PUT, DELETE
    allow_headers=["*"],
)
@app.get("/")
def home_page():
    cur.execute('''SELECT * FROM products''')
    data =  cur.fetchall()
    return {"message": data}

@app.post("/add_product")
def add_product(name: str, price: float):
    cur.execute('''INSERT INTO products (name, price) VALUES (?, ?)''', (name, price))
    con.commit()
    return {"message": "Product added successfully"}

@app.put("/update_product/{product_id}")
def update_product(product_id: int, name: str, price: float):
    cur.execute('''UPDATE products SET name = ?, price = ? WHERE id = ?''', (name, price, product_id))
    con.commit()
    return {"message": "Product updated successfully"}



@app.delete("/delete_product/{product_id}")
def delete_product(product_id: int):            
    
    cur.execute('''DELETE FROM products WHERE id = ?''', (product_id,))
    con.commit()
    return {"message": "Product deleted successfully"}      


