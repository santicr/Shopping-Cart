import sqlite3
DB_PATH = "/Users/santicr/Desktop/Github/Shopping-Cart/items.db"

#Función 1
# def verifyUser_(user, passw):
#     ans = 0
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     query1 = f"SELECT * FROM User WHERE Name = '{user}' AND Password = '{passw}'"
#     rows = cursor.execute(query1)
#     l = list(rows)
#     if len(l) == 1:
#         isAdmin = l[0][2]
#         if not isAdmin:
#             ans = 1
#         else:
#             ans = 2
#     conn.close()
#     return ans

#Función 2
# def deleteCartItem_(idIt, user):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     query1 = f"SELECT * FROM Cart WHERE ItemId = {idIt} AND User = '{user}'"
#     query2 = f"DELETE FROM Cart WHERE ItemId = {idIt} AND User = '{user}'"
#     row = list(cursor.execute(query1))
#     cant = row[0][2]
#     query3 = f"UPDATE Cart SET Quantity = {cant - 1} WHERE User = '{user}' AND ItemId = {idIt}"
#     if cant == 1:
#         cursor.execute(query2)
#     else:
#         cursor.execute(query3)
#     conn.commit()
#     conn.close()

# #Función 3
# def verifyPayCart_(itemId, quant):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     ans = True
#     query1 = f"""
#     SELECT Quantity
#     FROM Item
#     WHERE Id = {itemId}
#     """
#     lst = list(cursor.execute(query1))
#     qItem = int(lst[0][0])
#     if quant > qItem:
#         ans = False
#     else:
#         ans = True
#     conn.close()
#     return ans

#Función 4
# def existUser_(user):
#     ans = False
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     query1 = f"SELECT Name FROM User WHERE Name = '{user}'"
#     rows = cursor.execute(query1)
#     if len(list(rows)) == 0:
#         ans = True
#     conn.close()
#     return ans

#Función 5
def verifyUserPassword_(passw):
    ans = False
    flag1, flag2 = False, False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    special = {'!': 1, '@': 1, '#': 1, '$': 1, '%': 1, '^': 1, '&': 1, '*': 1, '(': 1, ')' : 1}
    if(len(passw) >= 8):
        i = 0
        while(i < len(passw)):
            c = passw[i]
            if c in special:
                flag1 = True
            if c in abc:
                flag2 = True
            i += 1
    else:
        ans = False
    if flag1 and flag2:
        ans = True
    return ans

# #Función 6
# def discount_(ccnum, hour, total):
#     ans = [0, 0]
#     if ccnum[-1] == hour:
#         total -= total * (float(hour) / 100)
#         ans[0] = (float(hour) / 100)
#     if int(ccnum[-1]) + int(ccnum[0]) > 4:
#         ans[1] = (total * 0.08)
#         total -= (total * 0.08)
    
#     return ans, total