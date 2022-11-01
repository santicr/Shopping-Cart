import pathlib
from typing import Union
import sqlite3
from fastapi import FastAPI

DB_PATH = "/Users/santicr/Desktop/Github/Shopping-Cart/items.db"

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "User"}

"""
Function to see if an user exists.
Input: User
Output: True if exists, otherwise, false.
"""
@app.get("/api/users/exist/{user}")
async def get_user(user: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT Name FROM User WHERE Name = '{user}'"
    rows = cursor.execute(query1)
    ans = True if not len(list(rows)) else False
    cursor.close()
    conn.close()
    return {f'{user}': ans}

"""
Function to verify password security requirements
Input: Password
Output: True if password meets requirements, otherwise, false
"""
@app.get("/api/users/verify/{password}")
async def verify_user_pass(password: str):
    ans = False
    flag1, flag2 = False, False
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    special = {'!': 1, '@': 1, '#': 1, '$': 1, '%': 1, '^': 1, '&': 1, '*': 1, '(': 1, ')': 1}
    if(len(password) >= 8):
        for i in range(len(password)):
            c = password[i]
            if c in special:
                flag1 = True
            if c in abc:
                flag2 = True
    else:
        ans = False
    ans = True if flag1 and flag2 else ans
    return {"Password": ans}

"""
Function to verify if user and password are in db (also if user is admin or user)
Input: User and password
Output: An integer representing if user exists, if its user or if its admin
"""
@app.get("/api/users/user/{user}/{passw}")
async def get_user_and_pass(user: str, passw: str):
    ans = 0
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT * FROM User WHERE Name = '{user}' AND Password = '{passw}'"
    rows = cursor.execute(query1)
    l = list(rows)
    ans = 0 if len(l) == 0 else l[0][2] + 1
    cursor.close()
    conn.close()
    return {f'{user}': ans}

"""
Function to insert user and password
Input: User and password to insert
"""
@app.post("/api/users/user/{user}/{passw}")
async def register_user(user: str, passw: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"INSERT INTO User VALUES('{user}', '{passw}', 0)"
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {"User": user}

"""
Function to read user address.
Input: An user
Output: A list with address and city info
"""
@app.get("/api/users/address/{user}")
async def get_user_address(user: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"SELECT Address, City FROM ClientAd WHERE User = '{user}'"
    lst = list(cursor.execute(query1))
    cursor.close()
    conn.close()
    return lst

"""
Function to insert user address
Input: An user and its address info/data
Output: None
"""
@app.post("/api/users/address/{user}")
async def register_user_address(user: str, data: list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"""
    INSERT INTO ClientAd(User, Address, City, Phone)
    VALUES('{user}', '{data[0]}', '{data[1]}', '{data[2]}')
    """
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {user: data}

@app.put("/api/users/address/{user}")
async def update_user_address(user: str, data: list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query1 = f"""
    UPDATE ClientAd SET Address = '{data[0]}', City = '{data[1]}', Phone = '{data[2]}'
    WHERE User = '{user}'
    """
    cursor.execute(query1)
    conn.commit()
    cursor.close()
    conn.close()
    return {user: data}