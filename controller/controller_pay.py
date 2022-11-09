import psycopg2
from datetime import datetime
import uuid
import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller/models')
from models import PayData
from controller_item import fetch_item_quantity, update_item_quantity
from controller_cart import delete_cart_user, fetch_cart_items, fetch_cart_user
from fastapi import APIRouter

app = APIRouter(
    tags = ["Pay"]
)

@app.get("/")
async def root():
    return {"Hello": "Pay"}

"""
Function to verify if a product in the cart has quantity <= actual quantity in db when paying
Input: Id of the product and product quantity in cart.
"""
@app.get("/api/payments/verify/{item_id}/{quant}")
async def verify_item_quant(item_id: int, quant: int):
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
    lst = list(cursor.execute(query1))
    qItem = int(lst[0][0])
    ans = False if quant > qItem else True
    cursor.close()
    conn.close()
    return {item_id: ans}

"""
Function to apply discounts when paying
Input: Credit card number, hour of paying and total amount of paying
Output: How many discounts where applied and the total amount of paying when discounts applied
"""
@app.get("/api/payments/discount/{ccnum}/{hour}/{total}")
def fetch_payment_discount(ccnum: str, hour: str, total: float):
    ans = [0, 0]
    if int(hour) >= 12:
        hour = int(hour)
        hour -= 12
        hour = str(hour)
    if ccnum[-1] == hour:
        ans[0] = total * (float(hour) / 100)
        total -= total * (float(hour) / 100)
    if int(ccnum[-1]) + int(ccnum[0]) > 4:
        ans[1] = (total * 0.08)
        total -= (total * 0.08)
    
    return sum(ans), total

"""
Function to pay all from cart:
First: Reads all cart items from an user.
Second: Updates the quantity from an item in db.
Third: Insert into Bill table, all information about the bill of the user.
"""
@app.get("/api/payments/process/{user}/{ccnum}/{total}")
def fetch_payment_process(user: str, ccnum: str, total: float):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    now = datetime.now()
    hour = now.strftime("%H")
    cursor = conn.cursor()
    lst1 = fetch_cart_user(user)
    lst1 = list(map(list, lst1))
    reference = str(uuid.uuid4())

    for el in lst1:
        item_id = el[1]
        cant1 = el[2]
        cant2 = fetch_item_quantity(item_id)
        new_cant = cant2 - cant1
        update_item_quantity(item_id, new_cant)
        query7 = f"""
        INSERT INTO Bill (user_web, Item, Quantity, Reference, Total)
        VALUES ('{user}', {item_id}, {cant1}, '{reference}', 0)
        """
        cursor.execute(query7)

    query2 = f"""
    SELECT Balance
    FROM UserCard
    WHERE CCnum = '{ccnum}'
    """
    query1 = f"""
    DELETE FROM Cart WHERE user_web = '{user}'
    """
    cursor.execute(query1)
    lst = list(cursor.execute(query2))
    ans, total = fetch_payment_discount(ccnum, hour, total)
    query3 = f"""
    UPDATE UserCard
    SET Balance = {lst[0][0] - total}
    WHERE CCnum = '{ccnum}'
    """
    query4 = f"""
    UPDATE Bill
    SET Total = {total}
    WHERE Reference = '{reference}'
    """
    cursor.execute(query3)
    cursor.execute(query4)
    conn.commit()
    cursor.close()
    conn.close()
    return ans

"""
Function to verify that the data of a credit card is valid
Input: All CreditCard fields, name, number, lastname, ccv
Output: Balance of that creditcard
"""
@app.get("/api/payments/verify/card")
def verify_card(name: str, lastname1: str, lastname2: str, ccnum: str, ccv: str):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    SELECT Balance
    FROM UserCard
    WHERE Name = '{name}' AND LastName1 = '{lastname1}'
    AND LastName2 = '{lastname2}' AND CCNum = '{ccnum}' AND CCV = '{ccv}'
    """
    lst = list(cursor.execute(query1))
    ans = (False, 0) if not len(lst) else (True, lst[0][0])
    return ans

@app.get("/api/payments/verify/products")
def verify_products(products: list):
    total = 0
    flag = True
    for p in products:
        flag = verify_item_quant(p[3], p[1])
        total += p[2]
    return (total, flag)

@app.get("/api/payments/pay")
def pay(pay_data: PayData):
    ans = 0
    total = 0
    flag_pay = True
    card_flag, balance = verify_card(pay_data.name, pay_data.lname1, pay_data.lname2, pay_data.ccnum, pay_data.ccv)
    products = fetch_cart_items(pay_data.user_name)
    total, flag_pay = verify_products(products)
    
    if card_flag:
        ans = 1
        if flag_pay:
            ans = 2
            if balance >= total:
                ans = 3
                res = fetch_payment_process(pay_data.user_name, pay_data.ccnum, total)
                if res:
                    ans = res
    return ans