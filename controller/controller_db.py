import psycopg2
from controller_item import readItemById
import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller/models')
from models import UserName, Reference
from fastapi import APIRouter

DB_PATH = "/Users/santicr/Desktop/Github/Shopping-Cart/items.db"

app = APIRouter(
    tags = ["Auxiliar db funcs"]
)

"""
Function to create all tables for db items
"""
def createTable():
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
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
        User TEXT, Item INT, Quantity INT, Reference TEXT, Total REAL,
        FOREIGN KEY(User) REFERENCES User(Name),
        FOREIGN KEY(Item) REFERENCES Item(Id)
        )
    """
    cursor.execute(query1)
    conn.commit()
    conn.close()

"""
Function to delete a table.
INPUT: Table name
"""
def deleteTable(name):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    conn.execute(f"DELETE FROM {name}")
    conn.commit()
    conn.close()

def insertCreditCard():
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    INSERT INTO UserCard
    (Name, LastName1, LastName2, CCNum, CCV, Balance)
    Values ('Santiago', 'Caicedo', 'Rojas', '012345678901234', '783', 1000000)
    """
    cursor.execute(query1)
    conn.commit()
    conn.close()

@app.get('/api/auxiliaries/ref')
def fetch_references(user_name: UserName):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    SELECT Reference
    FROM Bill
    WHERE user_web = '{user_name.user_name}'
    ORDER BY id DESC
    """
    cursor.execute(query1)
    rows = cursor.fetchall()
    lst = []
    for l in rows:
        lst.append(l[0])
    cursor.close()
    conn.close()
    return lst

"""
Function to search a buy reference
Input: The reference
Output: Name and quantity of each product bought with the reference
"""
@app.get('/api/auxiliaries/search')
def fetch_search_reference(ref: Reference):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    SELECT Item, Quantity, Total
    FROM Bill
    WHERE Reference = '{ref.reference}'
    """
    if len(ref.reference) == 0:
        return "No ingresaste nada, intenta de nuevo"
    cursor.execute(query1)
    lst = cursor.fetchall()
    if not len(lst):
        return "La referencia no existe, intenta de nuevo"
    data = []
    for el in lst:
        temp = readItemById(el[0])
        data.append([temp[0][1], el[1], temp[0][3], el[2]])
    return data

@app.get('/api/auxiliaries/bought')
def fetch_products_bought(user_name: UserName):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    SELECT Name, Bill.Quantity
    FROM Bill JOIN Item ON(Bill.Item = Item.Id)
    WHERE user_web = '{user_name.user_name}'
    ORDER BY Bill.Id DESC LIMIT 10
    """
    cursor.execute(query1)
    lst = cursor.fetchall()
    print(lst)
    cursor.close()
    conn.close()
    return lst
