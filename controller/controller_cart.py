from fastapi import APIRouter
import psycopg2
import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller/models')
from models import CartItem, CartItemUpdate

app = APIRouter(
    tags = ["cart"]
)

@app.get("/api/cart/user")
def fetch_cart_user(user: str):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Cart WHERE user_web = '{user}'"
    cursor.execute(query1)
    lst = cursor.fetchall()
    cursor.close()
    conn.close()
    return lst

@app.post("/api/cart/item")
def register_cart_item(cart_item: CartItem):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    INSERT INTO Cart VALUES('{cart_item.user_name}', {cart_item.item_id}, 1)
    """
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {cart_item.user_name: cart_item.item_id}

@app.delete('/api/cart/user')
def delete_cart_user(user: str):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    DELETE FROM Cart WHERE user_web = '{user}'
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {"Cart deleted": user}

@app.put("/api/cart/item")
def update_cart_item(new_item_cart: CartItemUpdate):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    UPDATE Cart SET Quantity = {new_item_cart.new_quant}
    WHERE user_web = '{new_item_cart.user_name}' AND ItemId = {new_item_cart.item_id}
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {new_item_cart.item_id: new_item_cart.new_quant}

"""
Function to delete one element of a cart from an user
Input: Item id and user
Output: None
"""
@app.get("/api/cart/item")
def fetch_cart_item(cart_item: CartItem):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Cart WHERE ItemId = {cart_item.item_id} AND user_web = '{cart_item.user_name}'"
    cursor.execute(query1)
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    return row

@app.delete("/api/cart/item")
def delete_cart_item(cart_item: CartItem):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"DELETE FROM Cart WHERE ItemId = {cart_item.item_id} AND user_web = '{cart_item.user_name}'"
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {"Deleted": [cart_item.user_name, cart_item.item_id]}

"""
Function to delete all from Cart table where user is matched
Input: User
"""
def deleteCart(userId):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"DELETE FROM Cart WHERE user_web = '{userId}'"
    cursor.execute(query1)
    conn.commit()
    conn.close()

"""
Function to read all items from an user cart
Input: User
Output: Rows with all information about an item of a cart
"""
@app.get("/api/cart/items/{user}")
def fetch_cart_items(user: str):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    SELECT Name, Cart.Quantity, Cart.Quantity * Price, ItemId
    FROM Cart INNER JOIN Item ON Id = ItemId WHERE user_web = '{user}'
    """
    cursor.execute(query1)
    rows = cursor.fetchall()
    conn.close()
    return rows

"""
Verify if I can add an item to an user cart
Input: Item
Output: True if I can add the item to an user cart, otherwise, false 
"""
@app.get("/api/cart/verify/{item_id}")
def fetch_verify_cart(item_id: int):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    ans = True
    query1 = f"""
    SELECT Quantity
    FROM Item
    WHERE Id = '{item_id}'
    """
    cursor.execute(query1)
    lst = cursor.fetchall()
    quant = int(lst[0][0])
    ans = False if quant <= 0 else ans
    cursor.close()
    conn.close()
    return ans