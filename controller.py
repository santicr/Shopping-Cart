import sqlite3

def createDB():
    conn = sqlite3.connect('items.db')
    conn.commit()
    conn.close()

def createTable():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    query1 = 'CREATE TABLE Items (Id varchar PRIMARY KEY, Name VARCHAR, Quantity INT, Price REAL)'
    cursor.execute(query1)
    conn.commit()
    conn.close()

def main():
    createTable()
    pass

main()