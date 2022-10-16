import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller')
from c import *
import unittest, sqlite3
DB_PATH = '/Users/santicr/Desktop/Github/Shopping-Cart/items.db'

class Test1(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 3
        self.data = ["Santiago", "Caicedo", "Rojas", "012345678901234", "783"]
        self.user = "santicr23"
        self.balance = verifyCard(self.data)[1]
        self.products = readCartItems(self.user)
        self.products_quant = len(self.products)
        self.amount, self.flag_quant = verifyProductsCart(self.products)
        self.items = readItems()
        self.items_user = readCartItems(self.user)
        self.items_quant = []
        self.items_user_quant = []
        
        for it in self.items_user:
            for it2 in self.items:
                if it[2] == it2[0]:
                    self.items_quant.append(it2[2])
                    self.items_user_quant.append(it[1])

        self.assertEqual(verifyCard(self.data)[0], True)
        self.assertEqual(self.flag_quant, True)
        self.assertGreaterEqual(self.balance, self.amount)
    
    def test(self):
        ans = payment(self.data, self.user)
        self.assertGreaterEqual(ans, 3)
    
    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT Balance
        FROM UserCard
        WHERE id = {self.id}
        """
        query2 = f"""
        SELECT User
        FROM Cart
        WHERE User = '{self.user}'
        """

        lst = list(cursor.execute(query1))
        lst1 = list(cursor.execute(query2))
        self.items_new = readItems()
        self.items_new_quant = []
        self.new_products_quant = len(lst1)
        self.new_balance = lst[0][0]

        for it in self.items_user:
            for it2 in self.items_new:
                if it[2] == it2[0]:
                    self.items_new_quant.append(it2[2])

        self.assertEqual(self.new_products_quant, 0)
        self.assertEqual(verifyCard(self.data)[0], True)
        self.assertEqual(self.flag_quant, True)
        self.assertEqual(self.new_balance, self.balance - self.amount)
        for i in range(len(self.items_new_quant)):
            self.assertEqual(self.items_new_quant[i], self.items_quant[i])

class Test2(unittest.TestCase):
    def setUp(self) -> None:
        self.data = ["Pepito", "Perez", "Lozada", "012345678901234", "783"]
        self.user = "santicr21"
        self.products = readCartItems(self.user)
        self.products_quant = len(self.products)
        self.items = readItems()
        self.items_user = readCartItems(self.user)
        self.items_quant = []
        self.items_user_quant = []

        for it in self.items_user:
            for it2 in self.items:
                if it[2] == it2[0]:
                    self.items_quant.append(it2[2])
                    self.items_user_quant.append(it[1])

        self.assertEqual(verifyCard(self.data)[0], False)

    def test(self):
        ans = payment(self.data, self.user)
        self.assertEqual(ans, 0)
    
    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT User
        FROM Cart
        WHERE User = '{self.user}'
        """
        self.new_products_quant = len(list(cursor.execute(query1)))
        self.items_new = readItems()
        self.items_new_quant = []

        self.assertEqual(verifyCard(self.data)[0], False)
        self.assertEqual(self.new_products_quant, self.products_quant)
        for i in range(len(self.items_new_quant)):
            self.assertEqual(self.items_new_quant[i], self.items_quant[i])

class Test3(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 3
        self.data = ["Santiago", "Caicedo", "Rojas", "012345678901234", "783"]
        self.user = "santicr21"
        self.balance = verifyCard(self.data)[1]
        self.products = readCartItems(self.user)
        self.items = readItems()
        self.amount, self.flag_quant = verifyProductsCart(self.products)
        self.items_user = readCartItems(self.user)
        self.items_quant = []
        self.items_user_quant = []

        for it in self.items_user:
            for it2 in self.items:
                if it[2] == it2[0]:
                    self.items_quant.append(it2[2])
                    self.items_user_quant.append(it[1])

        self.assertEqual(verifyCard(self.data)[0], True)
        self.assertEqual(self.flag_quant, False)

    def test(self):
        ans = payment(self.data, self.user)
        self.assertEqual(ans, 1)
    
    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT Balance
        FROM UserCard
        WHERE id = {self.id}
        """
        lst = list(cursor.execute(query1))
        self.new_balance = lst[0][0]
        self.items_new = readItems()
        self.items_new_quant = []

        self.assertEqual(self.new_balance, self.balance)
        self.assertEqual(verifyCard(self.data)[0], True)
        self.assertEqual(self.flag_quant, False)

        for i in range(len(self.items_new_quant)):
            self.assertEqual(self.items_new_quant[i], self.items_quant[i])

class Test4(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 1
        self.data = ["Santiago", "Caicedo", "Rojas", "12345678901234", "783"]
        self.user = "santiago"
        self.balance = verifyCard(self.data)[1]
        self.products = readCartItems(self.user)
        self.items = readItems()
        self.amount, self.flag_quant = verifyProductsCart(self.products)
        self.items_user = readCartItems(self.user)
        self.items_quant = []
        self.items_user_quant = []

        for it in self.items_user:
            for it2 in self.items:
                if it[2] == it2[0]:
                    self.items_quant.append(it2[2])
                    self.items_user_quant.append(it[1])

        self.assertEqual(verifyCard(self.data)[0], True)
        self.assertEqual(self.flag_quant, True)
        self.assertGreater(self.amount, self.balance)

    def test(self):
        ans = payment(self.data, self.user)
        self.assertEqual(ans, 2)

    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT Balance
        FROM UserCard
        WHERE id = {self.id}
        """
        lst = list(cursor.execute(query1))
        self.new_balance = lst[0][0]
        self.items_new = readItems()
        self.items_new_quant = []
        
        self.assertEqual(self.new_balance, self.balance)
        self.assertEqual(verifyCard(self.data)[0], True)
        self.assertEqual(self.flag_quant, True)

        for i in range(len(self.items_new_quant)):
            self.assertEqual(self.items_new_quant[i], self.items_quant[i])