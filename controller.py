import sqlite3
from datetime import datetime

def createTable():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = 'CREATE TABLE Item(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Quantity INT, Price REAL, Sold INT, Description TEXT, URL TEXT)'
    query2 = """
    CREATE TABLE Cart(
        User TEXT, ItemId INTEGER, Quantity INTEGER, FOREIGN KEY(User) REFERENCES User(Name), FOREIGN KEY(ItemId) REFERENCES Item(Id), PRIMARY KEY(User, ItemId)
    )
    """
    query3 = "CREATE TABLE ClientAd (Id INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT, Address TEXT, City TEXT, Phone TEXT, FOREIGN KEY(User) REFERENCES User(NAME))"
    query4 = "CREATE TABLE UserCard (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, LastName1 TEXT, LastName2 TEXT, CCNum TEXT, CCV TEXT, Balance REAL)"
    query5 = """
    CREATE TABLE Bill (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        User TEXT, Item INT, Quantity INT,
        FOREIGN KEY(User) REFERENCES User(Name),
        FOREIGN KEY(Item) REFERENCES Item(Id)
        )
    """
    cursor.execute(query5)
    conn.commit()
    conn.close()

def deleteTable():
    conn = sqlite3.connect('items.db')
    conn.execute("DROP TABLE UserCard")
    conn.commit()
    conn.close()

def insertItem(data):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"INSERT INTO Item (Name, Quantity, Price, Sold, Description, URL) VALUES('{data[0]}', {data[1]}, {data[2]}, {data[3]}, '{data[4]}', '{data[5]}')"
    cursor.execute(query1)
    conn.commit()
    conn.close()

def readItem():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = "SELECT * FROM item"
    rows = list(cursor.execute(query1))
    return rows

def readUser(user):
    ans = False
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"SELECT Name FROM User WHERE Name = '{user}'"
    rows = cursor.execute(query1)
    if len(list(rows)) == 0:
        ans = True
    conn.close()
    return ans

def readCart(user):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Cart WHERE User = '{user}'"
    rows = cursor.execute(query1)
    lst = list(rows)
    conn.close()
    return lst

def insertUser(user, passw):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"INSERT INTO User VALUES('{user}', '{passw}', 0)"
    cursor.execute(query1)
    conn.commit()
    conn.close()

def insertCart(userId, itemId):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"INSERT INTO Cart VALUES('{userId}', {itemId}, 1)"
    query2 = f"SELECT * FROM Cart WHERE User = '{userId}' AND ItemId = {itemId}"
    rows = cursor.execute(query2)
    lst = list(rows)
    if not len(lst):
        cursor.execute(query1)
    else:
        query3 = f"UPDATE Cart SET Quantity = {lst[0][2] + 1} WHERE User = '{userId}' AND ItemId = {itemId}"
        cursor.execute(query3)
    conn.commit()
    conn.close()

def deleteCartItem(userId):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"DELETE FROM Cart WHERE User = '{userId}'"
    cursor.execute(query1)
    conn.commit()
    conn.close()

def existUser(user, passw):
    ans = 0
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"SELECT * FROM User WHERE Name = '{user}' AND Password = '{passw}'"
    rows = cursor.execute(query1)
    l = list(rows)
    if len(l) == 1:
        isAdmin = l[0][2]
        if isAdmin == 0:
            ans = 1
        elif isAdmin == 1:
            ans = 2
    conn.close()
    return ans
    
def readCartItems(user):
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    query1 = f"SELECT Name, Cart.Quantity, Cart.Quantity * Price, ItemId FROM Cart INNER JOIN Item ON Id = ItemId WHERE User = '{user}'"
    rows = cursor.execute(query1)
    rows = list(rows)
    conn.close()
    return rows

"""
Function to read an item.
Input: Item id.
"""
def readItemById(idIt):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Item where id = {idIt}"
    row = list(cursor.execute(query1))
    conn.close()
    return row

"""
Function to delete one element of a cart from an user
Input: Item id and user
Output: None
"""
def deleteCart(idIt, user):
    conn = sqlite3.connect('items.db')
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
Function to insert user address
Input: An user and its address info/data
Output: None
"""
def insertAddress(user, data):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"SELECT User FROM ClientAd WHERE User = '{user}'"
    query2 = f"INSERT INTO ClientAd(User, Address, City, Phone) VALUES('{user}', '{data[0]}', '{data[1]}', '{data[2]}')"
    lst = list(cursor.execute(query1))
    if len(lst) == 0:
        cursor.execute(query2)
    else:
        query3 = f"UPDATE ClientAd SET Address = '{data[0]}', City = '{data[1]}', Phone = '{data[2]}' WHERE User = '{user}'"
        cursor.execute(query3)
    conn.commit()
    conn.close()

"""
Function to read user address.
Input: An user
Output: A list with all address info (city, address, phone, etc)
"""
def readAdd(user):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"SELECT Address, City FROM ClientAd WHERE User = '{user}'"
    lst = list(cursor.execute(query1))
    conn.close()
    return lst

"""
Function to insert a credit_card as an example, no parameters.
"""
def insertCc():
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    query1 = """
    INSERT INTO UserCard (Name, LastName1, LastName2, CCNum, CCV, Balance)
    VALUES ('Santiago', 'Caicedo', 'Rojas', '12345678901235', '783', 1000000.0)
    """
    cursor.execute(query1)
    conn.commit()
    conn.close()

def verifyCard(data):
    ans = False, 0
    conn = sqlite3.connect("items.db")
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

def discount(ccnum, hour, total):
    ans = [0, 0]
    if ccnum[-1] == hour:
        total -= total * (float(hour) / 100)
        ans[0] = (float(hour) / 100)
    if int(ccnum[-1]) + int(ccnum[0]) > 4:
        total = total - (total * 0.08)
        ans[1] = (total * 0.08)
    
    return ans, total

def payFunc(user, ccnum, total):
    conn = sqlite3.connect("items.db")
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

def itemsToShow(itemId, quant2):
    ans = quant2
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    query1 = f"SELECT Quantity FROM Item WHERE Id = {itemId}"
    lst = list(cursor.execute(query1))
    if len(lst) > 0:
        quant = int(lst[0][0])
        ans = quant - quant2
    conn.close()
    return ans

def main():
    #createTable()
    #insertCc()
    pass

main()