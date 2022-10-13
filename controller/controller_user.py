import sqlite3

DB_PATH = "/Users/santicr/Desktop/Github/Shopping-Cart/items.db"

"""
Function to see if an user exists.
Input: User
Output: True if exists, otherwise, false.
"""
def existUser(user):
    ans = False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT Name FROM User WHERE Name = '{user}'"
    rows = cursor.execute(query1)
    if len(list(rows)) == 0:
        ans = True
    conn.close()
    return ans

"""
Function to verify if user and password are in db (also if user is admin or user)
Input: User and password
Output: An integer representing if user exists, if its user or if its admin
"""
def verifyUser(user, passw):
    ans = 0
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT * FROM User WHERE Name = '{user}' AND Password = '{passw}'"
    rows = cursor.execute(query1)
    l = list(rows)
    if len(l) == 1:
        isAdmin = l[0][2]
        if not isAdmin:
            ans = 1
        else:
            ans = 2
    conn.close()
    return ans

"""
Function to insert user and password
Input: User and password to insert
"""
def insertUser(user, passw):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"INSERT INTO User VALUES('{user}', '{passw}', 0)"
    cursor.execute(query1)
    conn.commit()
    conn.close()

"""
Function to read user address.
Input: An user
Output: A list with all address info (city, address, phone, etc)
"""
def readUserAddress(user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT Address, City FROM ClientAd WHERE User = '{user}'"
    lst = list(cursor.execute(query1))
    conn.close()
    return lst

"""
Function to insert user address
Input: An user and its address info/data
Output: None
"""
def insertUserAddress(user, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT User FROM ClientAd WHERE User = '{user}'"
    query2 = f"""
    INSERT INTO ClientAd(User, Address, City, Phone)
    VALUES('{user}', '{data[0]}', '{data[1]}', '{data[2]}')
    """
    lst = list(cursor.execute(query1))
    if len(lst) == 0:
        cursor.execute(query2)
    else:
        query3 = f"""
        UPDATE ClientAd SET Address = '{data[0]}', City = '{data[1]}', Phone = '{data[2]}'
        WHERE User = '{user}'
        """
        cursor.execute(query3)
    conn.commit()
    conn.close()