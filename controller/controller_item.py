import sqlite3

DB_PATH = '/Users/santicr/Desktop/Github/Shopping-Cart/items.db'

"""
Function to insert a row to Item table
INPUT: Row
"""
def insertItem(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"""
    INSERT INTO Item (Name, Quantity, Price, Sold, Description, URL)
    VALUES('{data[0]}', {data[1]}, {data[2]}, {data[3]}, '{data[4]}', '{data[5]}')
    """
    cursor.execute(query1)
    conn.commit()
    conn.close()

"""
Function to read an item.
Input: Item id.
Output: Row with Item info.
"""
def readItemById(idIt):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT * FROM Item where id = {idIt}"
    row = list(cursor.execute(query1))
    conn.close()
    return row

"""
Function to read all rows from Item table.
Output: All rows of Item table.
"""
def readItems():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = "SELECT * FROM item"
    rows = list(cursor.execute(query1))
    return rows

def itemsToShow(itemId, quant2):
    ans = quant2
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT Quantity FROM Item WHERE Id = {itemId}"
    lst = list(cursor.execute(query1))
    if len(lst) > 0:
        quant = int(lst[0][0])
        ans = quant - quant2
    conn.close()
    return ans