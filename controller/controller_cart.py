import sqlite3

DB_PATH = "/Users/santicr/Desktop/Github/Shopping-Cart/items.db"

def readCart(user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Cart WHERE User = '{user}'"
    rows = cursor.execute(query1)
    lst = list(rows)
    conn.close()
    return lst

def insertCart(userId, itemId):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"INSERT INTO Cart VALUES('{userId}', {itemId}, 1)"
    query2 = f"SELECT * FROM Cart WHERE User = '{userId}' AND ItemId = {itemId}"
    rows = cursor.execute(query2)
    lst = list(rows)
    if not len(lst):
        cursor.execute(query1)
    else:
        query3 = f"""
        UPDATE Cart SET Quantity = {lst[0][2] + 1}
        WHERE User = '{userId}' AND ItemId = {itemId}
        """
        cursor.execute(query3)
    conn.commit()
    conn.close()

"""
Function to delete one element of a cart from an user
Input: Item id and user
Output: None
"""
def deleteCartItem(idIt, user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Cart WHERE ItemId = {idIt} AND User = '{user}'"
    query2 = f"DELETE FROM Cart WHERE ItemId = {idIt} AND User = '{user}'"
    row = list(cursor.execute(query1))
    cant = row[0][2]
    query3 = f"UPDATE Cart SET Quantity = {cant - 1} WHERE User = '{user}' AND ItemId = {idIt}"
    if cant == 1:
        cursor.execute(query2)
    elif cant > 1:
        cursor.execute(query3)
    conn.commit()
    conn.close()

"""
Function to delete all from Cart table where user is matched
Input: User
"""
def deleteCart(userId):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"DELETE FROM Cart WHERE User = '{userId}'"
    cursor.execute(query1)
    conn.commit()
    conn.close()

"""
Function to read all items from an user cart
Input: User
Output: Rows with all information about an item of a cart
"""
def readCartItems(user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"""
    SELECT Name, Cart.Quantity, Cart.Quantity * Price, ItemId
    FROM Cart INNER JOIN Item ON Id = ItemId WHERE User = '{user}'
    """
    rows = cursor.execute(query1)
    rows = list(rows)
    conn.close()
    return rows

"""
Verify if I can add an item to an user cart
Input: Item
Output: True if I can add the item to an user cart, otherwise, false 
"""
def verifyCartAdd(itemId):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ans = True
    query1 = f"""
    SELECT Quantity
    FROM Item
    WHERE Id = '{itemId}'
    """
    lst = list(cursor.execute(query1))
    quant = int(lst[0][0])
    if quant == 0:
        ans = False
    conn.close()
    return ans