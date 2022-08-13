import sqlite3

def createTable():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = 'CREATE TABLE Item(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Quantity INT, Price REAL, Sold INT, Description TEXT, URL TEXT)'
    query2 = """
    CREATE TABLE Cart(
        User TEXT, ItemId INTEGER, FOREIGN KEY(User) REFERENCES User(Name), FOREIGN KEY(ItemId) REFERENCES Item(Id)
    )
    """
    cursor.execute(query2)
    conn.commit()
    conn.close()

def deleteTable():
    conn = sqlite3.connect('items.db')
    conn.execute("DROP TABLE Item")
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
    rows = cursor.execute(query1)
    print(rows)
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
    lrows = len(list(rows))
    conn.close()
    return lrows

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
    query1 = f"INSERT INTO Cart VALUES('{userId}', {itemId})"
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
    query1 = f"SELECT ItemId FROM Cart WHERE User = '{user}'"
    rows = cursor.execute(query1)
    rows = list(rows)
    conn.close()
    return rows

def readItemById(idIt):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Item where id = {idIt}"
    row = list(cursor.execute(query1))
    conn.close()
    return row

def main():
    #deleteTable()
    #createTable()
    #existUser('santicr', '1')
    #readCart("santicr21")
    pass

main()