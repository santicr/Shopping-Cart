import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller')
from c import *
import unittest, sqlite3
DB_PATH = '/Users/santicr/Desktop/Github/Shopping-Cart/items.db'

class Test1(unittest.TestCase):
    def setUp(self) -> None:
        self.user = "santicr"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT Admin
        FROM User
        WHERE Name = '{self.user}'
        """
        query2 = """
        SELECT *
        FROM Item
        """
        self.item_length = len(list(cursor.execute(query2)))
        self.admin = list(cursor.execute(query1))[0][0]
        self.product_name = "Cade"
        self.quant = 1
        self.price = 500
        self.description = "Prueba de caso"

        self.assertEqual(self.admin, 1)
        self.assertLess(len(self.product_name), 5)
        conn.close()

    def test(self):
        data = [self.product_name, self.quant, self.price, 0, self.description]
        ans = verifyItemInsert(data)
        self.assertEqual(ans, 0)

    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT *
        FROM Item
        """
        self.items_new_length = len(list(cursor.execute(query1)))
        conn.close()
        
        self.assertEqual(self.admin, 1)
        self.assertLess(len(self.product_name), 5)
        self.assertEqual(self.item_length, self.items_new_length)

class Test2(unittest.TestCase):
    def setUp(self) -> None:
        self.user = "santicr"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT Admin
        FROM User
        WHERE Name = '{self.user}'
        """
        query2 = """
        SELECT *
        FROM Item
        """
        self.item_length = len(list(cursor.execute(query2)))
        self.admin = list(cursor.execute(query1))[0][0]
        self.product_name = "Cadena"
        self.quant = 0
        self.price = 500
        self.description = "Prueba de caso"

        self.assertEqual(self.admin, 1)
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertLessEqual(self.quant, 0)
        conn.close()

    def test(self):
        data = [self.product_name, self.quant, self.price, 0, self.description]
        ans = verifyItemInsert(data)
        self.assertEqual(ans, 1)

    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT *
        FROM Item
        """
        self.items_new_length = len(list(cursor.execute(query1)))
        conn.close()
        
        self.assertEqual(self.admin, 1)
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertLessEqual(self.quant, 0)
        self.assertEqual(self.item_length, self.items_new_length)

class Test3(unittest.TestCase):
    def setUp(self) -> None:
        self.user = "santicr"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT Admin
        FROM User
        WHERE Name = '{self.user}'
        """
        query2 = """
        SELECT *
        FROM Item
        """
        self.item_length = len(list(cursor.execute(query2)))
        self.admin = list(cursor.execute(query1))[0][0]
        self.product_name = "Cadena"
        self.quant = 5
        self.price = 459
        self.description = "Prueba de caso"

        self.assertEqual(self.admin, 1)
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreaterEqual(self.quant, 1)
        self.assertLess(self.price, 500)
        conn.close()

    def test(self):
        data = [self.product_name, self.quant, self.price, 0, self.description]
        ans = verifyItemInsert(data)
        self.assertEqual(ans, 2)

    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT *
        FROM Item
        """
        self.items_new_length = len(list(cursor.execute(query1)))
        conn.close()
        
        self.assertEqual(self.admin, 1)
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quant, 0)
        self.assertLess(self.price, 500)
        self.assertEqual(self.item_length, self.items_new_length)

class Test4(unittest.TestCase):
    def setUp(self) -> None:
        self.user = "santicr"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT Admin
        FROM User
        WHERE Name = '{self.user}'
        """
        query2 = """
        SELECT *
        FROM Item
        """
        self.item_length = len(list(cursor.execute(query2)))
        self.admin = list(cursor.execute(query1))[0][0]
        self.product_name = "Cadena"
        self.quant = 5
        self.price = 600
        self.description = "Prue"

        self.assertEqual(self.admin, 1)
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreaterEqual(self.quant, 1)
        self.assertGreaterEqual(self.price, 500)
        self.assertLess(len(self.description), 5)
        conn.close()

    def test(self):
        data = [self.product_name, self.quant, self.price, 0, self.description]
        ans = verifyItemInsert(data)
        self.assertEqual(ans, 3)

    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT *
        FROM Item
        """
        self.items_new_length = len(list(cursor.execute(query1)))
        conn.close()
        
        self.assertEqual(self.admin, 1)
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quant, 0)
        self.assertGreaterEqual(self.price, 500)
        self.assertLess(len(self.description), 5)
        self.assertEqual(self.item_length, self.items_new_length)

class Test5(unittest.TestCase):
    def setUp(self) -> None:
        self.user = "santicr"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT Admin
        FROM User
        WHERE Name = '{self.user}'
        """
        query2 = """
        SELECT *
        FROM Item
        """
        self.item_length = len(list(cursor.execute(query2)))
        self.admin = list(cursor.execute(query1))[0][0]
        self.product_name = "Cadensadsasdda"
        self.quant = 5
        self.price = 600
        self.description = "Prueba de cadena"

        self.assertEqual(self.admin, 1)
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreaterEqual(self.quant, 1)
        self.assertGreaterEqual(self.price, 500)
        self.assertGreaterEqual(len(self.description), 5)
        conn.close()

    def test(self):
        self.data = [self.product_name, self.quant, self.price, 0, self.description, '/static']
        ans = verifyItemInsert(self.data)
        self.assertEqual(ans, 4)

    def tearDown(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT *
        FROM Item
        """
        insertItem(self.data)
        self.items_new_length = len(list(cursor.execute(query1)))
        conn.close()
        
        self.assertEqual(self.admin, 1)
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quant, 0)
        self.assertGreaterEqual(self.price, 500)
        self.assertGreaterEqual(len(self.description), 5)
        self.assertGreater(self.items_new_length, self.item_length)