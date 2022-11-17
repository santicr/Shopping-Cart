import psycopg2
from fastapi import APIRouter
import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller/models')
from models import Item

app = APIRouter(
    tags = ["items"],
)

@app.get("/api/item/quantity/{item_id}")
def fetch_item_quantity(item_id: int):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    SELECT Quantity
    FROM Item
    WHERE Id = {item_id}
    """
    cursor.execute(query1)
    lst = cursor.fetchall()
    cursor.close()
    conn.close()
    return lst[0][0]

@app.put("/api/item/quantity/{item_id}")
def update_item_quantity(item_id: int, new_quantity: float):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    UPDATE Item
    SET Quantity = {new_quantity}
    WHERE Id = {item_id}
    """
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {item_id: new_quantity}

"""
Function to insert a row to Item table
INPUT: Row
"""
@app.post("/api/items")
def register_item(item: Item):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    INSERT INTO Item (Name, Quantity, Price, Sold, Description, URL)
    VALUES('{item.name}', {item.quant}, {item.price}, {item.sold}, '{item.desc}', '{item.file_upload}')
    """
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {item.name: item.quant}

"""
Function to read an item.
Input: Item id.
Output: Row with Item info.
"""
def readItemById(idIt):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Item where id = {idIt}"
    cursor.execute(query1)
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    return row

"""
Function to read all rows from Item table.
Output: All rows of Item table.
"""
@app.get("/api/items")
def fetch_items():
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = "SELECT * FROM item"
    cursor.execute(query1)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.get("/api/items/user")
def fetch_item_user(item_id: int, quant2: int):
    ans = quant2
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"SELECT Quantity FROM Item WHERE Id = {item_id}"
    cursor.execute(query1)
    lst = cursor.fetchall()
    if len(lst) > 0:
        quant = int(lst[0][0])
        ans = quant - quant2
    cursor.close()
    conn.close()
    return ans
    
"""
Function to verify if data given by admin is valid
Input: Name, quantity, price and description of a product
Output: Valid (4) or not valid (0, 1, 2, 3)
"""
@app.get("/api/items/verify/{name}/{quant}/{price}/{desc}")
def fetch_verify_item_insert(name: str, quant: int, price: float, desc: str):
    ans = 4
    if len(name) < 5:
        ans = 0
    elif quant <= 0:
        ans = 1
    elif price < 500:
        ans = 2
    elif len(desc) < 5:
        ans = 3
    return ans