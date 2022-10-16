import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller')
from c import *
import unittest, sqlite3
DB_PATH = '/Users/santicr/Desktop/Github/Shopping-Cart/items.db'

class Test1(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = ""
        self.assertEqual(self.reference, "")

    def test(self):
        ans = searchReference(self.reference)
        self.assertEqual(ans, "No ingresaste nada, intenta de nuevo")
    
    def tearDown(self) -> None:
        self.assertEqual(self.reference, "")

class Test2(unittest.TestCase):
    def setUp(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        self.reference = "asodjasdn"
        cursor = conn.cursor()
        query1 = f"""
        SELECT *
        FROM Bill
        WHERE Reference = '{self.reference}'
        """
        self.lst = list(cursor.execute(query1))
        
        self.assertEqual(len(self.lst), 0)

    def test(self):
        ans = searchReference(self.reference)
        self.assertEqual(ans, "La referencia no existe, intenta de nuevo")
    
    def tearDown(self) -> None:
        self.assertEqual(len(self.lst), 0)

class Test3(unittest.TestCase):
    def setUp(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        self.reference = "20b6a472-d0ae-4be9-b953-31744440d883"
        cursor = conn.cursor()
        query1 = f"""
        SELECT *
        FROM Bill
        WHERE Reference = '{self.reference}'
        """
        self.lst = list(cursor.execute(query1))
        
        self.assertGreaterEqual(len(self.lst), 1)

    def test(self):
        ans = searchReference(self.reference)
        self.assertEqual(type(ans), list)

    def tearDown(self) -> None:
        self.assertGreaterEqual(len(self.lst), 1)