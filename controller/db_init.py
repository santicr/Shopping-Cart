import os
import psycopg2

con = psycopg2.connect(
    host = "localhost",
    database = "items_db",
    user = 'postgres',
    password = 'admin'
)

cur = con.cursor()
# (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Quantity INT, Price REAL, Sold INT, Description TEXT, URL TEXT)
query1 = """
    CREATE TABLE item(
        id serial PRIMARY KEY,
        name varchar (150) NOT NULL,
        quantity int NOT NULL,
        price real NOT NULL,
        sold int NOT NULL,
        description text NOT NULL,
        url text NOT NULL
    );
"""
query2 = """
    CREATE TABLE user_web(
        name varchar (100) PRIMARY KEY,
        password varchar (100) NOT NULL,
        admin INT NOT NULL
    );
"""
query3 = """
    CREATE TABLE UserCard(
        id serial PRIMARY KEY,
        name varchar (100) NOT NULL,
        lastname1 varchar (100) NOT NULL,
        lastname2 varchar (100) NOT NULL,
        ccnum varchar (16) NOT NULL,
        ccv varchar (3) NOT NULL,
        balance real NOT NULL
    );
"""
query4 = """
    CREATE TABLE Bill (
        Id serial PRIMARY KEY,
        User_web TEXT, Item INT, Quantity INT, Reference TEXT, Total REAL,
        FOREIGN KEY(User_web) REFERENCES User_web(Name),
        FOREIGN KEY(Item) REFERENCES Item(Id)
    );
"""
query5 = """
CREATE TABLE ClientAd(
    id serial PRIMARY KEY,
    user_web TEXT,
    address TEXT,
    city TEXT,
    phone TEXT,
    FOREIGN KEY(user_web) REFERENCES User_web(name)
    );
"""
query6 = """
    CREATE TABLE Cart(
        user_web TEXT,
        itemId INT,
        quantity INT,
        FOREIGN KEY(user_web) REFERENCES user_web(Name),
        FOREIGN KEY(ItemId) REFERENCES item(Id),
        PRIMARY KEY(user_web, ItemId)
    )
"""
cur.execute(query3)
con.commit()
cur.close()
con.close()