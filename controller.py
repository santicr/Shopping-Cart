import sqlite3
from venv import create

def createDB():
    conn = sqlite3.connect('items.db')
    conn.commit()
    conn.close()

def createTable():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = 'CREATE TABLE Item (Id INT PRIMARY KEY, Name VARCHAR, Quantity INT, Price REAL, Sold INT\
        , Description TEXT)'
    cursor.execute(query1)
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
    query1 = f"INSERT INTO Item VALUES({data[0]}, '{data[1]}', {data[2]}, {data[3]}, {data[4]}, '{data[5]}')"
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

def main():
    #createTable()
    #deleteTable()
    readItem()
    pass

main()