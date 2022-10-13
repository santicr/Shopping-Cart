import sqlite3

DB_PATH = "/Users/santicr/Desktop/Github/Shopping-Cart/items.db"

"""
Function to create all tables for db items
"""
def createTable():
    conn = sqlite3.connect(DB_PATH)
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

"""
Function to delete a table.
INPUT: Table name
"""
def deleteTable(name):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"DROP TABLE {name}")
    conn.commit()
    conn.close()