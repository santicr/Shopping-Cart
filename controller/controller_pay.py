import sqlite3
from datetime import datetime
from controller_cart import deleteCart, readCartItems

DB_PATH = "/Users/santicr/Desktop/Github/Shopping-Cart/items.db"

"""
Function to verify if a product in the cart has quantity <= actual quantity in db when paying
Input: Id of the product and product quantity in cart.
"""
def verifyPayCart(itemId, quant):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ans = True
    query1 = f"""
    SELECT Quantity
    FROM Item
    WHERE Id = {itemId}
    """
    lst = list(cursor.execute(query1))
    qItem = int(lst[0][0])
    if quant > qItem:
        ans = False
    conn.close()
    return ans

"""
Function to apply discounts when paying
Input: Credit card number, hour of paying and total amount of paying
Output: How many discounts where applied and the total amount of paying when discounts applied
"""
def discount(ccnum, hour, total):
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
    
    return ans, total

"""
Function to pay all from cart:
First: Reads all cart items from an user.
Second: Updates the quantity from an item in db.
Third: Insert into Bill table, all information about the bill of the user.
"""
def payFunc(user, ccnum, total):
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now()
    hour = now.strftime("%H")
    cursor = conn.cursor()
    query4 = f"""
    SELECT *
    FROM Cart
    WHERE User = '{user}'
    """
    lst1 = list(cursor.execute(query4))
    lst1 = list(map(list, lst1))

    for el in lst1:
        itid = el[1]
        cant1 = el[2]
        query5 = f"""
        SELECT Quantity
        FROM Item
        WHERE Id = {itid}
        """
        tmp = list(cursor.execute(query5))
        tmp = list(map(list, tmp))
        cant2 = tmp[0][0]
        query6 = f"""
        UPDATE Item
        SET Quantity = {cant2 - cant1}
        WHERE Id = {itid} 
        """
        query7 = f"""
        INSERT INTO Bill (User, Item, Quantity)
        VALUES ('{user}', {itid}, {cant1})
        """
        cursor.execute(query6)
        cursor.execute(query7)

    query1 = f"""
    DELETE FROM Cart WHERE User = '{user}'
    """
    query2 = f"""
    SELECT Balance
    FROM UserCard
    WHERE CCnum = '{ccnum}'
    """
    cursor.execute(query1)
    lst = list(cursor.execute(query2))
    ans, total = discount(ccnum, hour, total)
    query3 = f"""
    UPDATE UserCard
    SET Balance = {lst[0][0] - total}
    WHERE CCnum = '{ccnum}'
    """
    cursor.execute(query3)
    conn.commit()
    conn.close()
    return ans

"""
Function to verify that the data of a credit card is valid
Input: All CreditCard fields, name, number, lastname, ccv
Output: Balance of that creditcard
"""
def verifyCard(data):
    ans = False, 0
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"""
    SELECT Balance
    FROM UserCard
    WHERE Name = '{data[0]}' AND LastName1 = '{data[1]}' AND LastName2 = '{data[2]}' AND CCNum = '{data[3]}' AND CCV = '{data[4]}' 
    """
    lst = list(cursor.execute(query1))
    if len(lst) == 1:
        ans = True, lst[0][0]
    return ans

def verifyProductsCart(products):
    total = 0
    flag = True
    for p in products:
        flag = verifyPayCart(p[3], p[1])
        total += p[2]
    return total, flag

def payment(data, user):
    ans = 0
    total = 0
    flag_pay = True
    card_flag, balance = verifyCard(data)
    products = readCartItems(user)
    total, flag_pay = verifyProductsCart(products)
    
    if card_flag:
        ans = 1
        if flag_pay:
            ans = 2
            if balance >= total:
                ans = 3
                res = payFunc(user, data[3], total)
                if res[0] or res[1]:
                    ans = 0
                    for r in res: ans += r
    return ans