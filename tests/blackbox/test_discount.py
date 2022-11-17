import sys
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller')
from controller_pay import fetch_payment_discount
import unittest, sqlite3
DB_PATH = '/Users/santicr/Desktop/Github/Shopping-Cart/items.db'

class Test1(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT CCNum
        FROM UserCard
        WHERE Id = {self.id}
        """
        self.total = 10000
        self.hour = '4'
        self.credit_card = list(cursor.execute(query1))[0][0]

        self.assertEqual(self.hour, self.credit_card[-1])
        self.assertLessEqual(int(self.credit_card[0]) + int(self.credit_card[1]), 4)

    def test(self):
        self.new_total = fetch_payment_discount(self.credit_card, self.hour, self.total)[1]
        self.assertEqual(self.new_total, self.total - (self.total * int(self.hour) / 100))
    
    def tearDown(self) -> None:
        self.assertEqual(self.hour, self.credit_card[-1])
        self.assertLessEqual(int(self.credit_card[0]) + int(self.credit_card[1]), 4)
        self.assertLess(self.total, self.new_total)

class Test2(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 2
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT CCNum
        FROM UserCard
        WHERE Id = {self.id}
        """
        self.total = 10000
        self.hour = '4'
        lst = list(cursor.execute(query1))
        self.credit_card = lst[0][0]

        self.assertNotEqual(self.hour, self.credit_card[-1])
        self.assertGreater(int(self.credit_card[0]) + int(self.credit_card[-1]), 4)
    
    def test(self):
        new_total = fetch_payment_discount(self.credit_card, self.hour, self.total)[1]
        self.assertEqual(new_total, self.total - (self.total * 0.08))
    
    def tearDown(self) -> None:
        self.assertNotEqual(self.hour, self.credit_card[-1])
        self.assertGreater(int(self.credit_card[0]) + int(self.credit_card[-1]), 4)

class Test3(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 2
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT CCNum
        FROM UserCard
        WHERE Id = {self.id}
        """
        self.total = 10000
        self.hour = '5'
        lst = list(cursor.execute(query1))
        self.credit_card = lst[0][0]

        self.assertEqual(self.hour, self.credit_card[-1])
        self.assertGreater(int(self.credit_card[0]) + int(self.credit_card[-1]), 4)
    
    def test(self):
        new_total = fetch_payment_discount(self.credit_card, self.hour, self.total)[1]
        fp = self.total - (self.total * (int(self.hour) / 100))
        self.assertEqual(new_total, fp - fp * 0.08)
    
    def tearDown(self) -> None:
        self.assertEqual(self.hour, self.credit_card[-1])
        self.assertGreater(int(self.credit_card[0]) + int(self.credit_card[-1]), 4)

class Test4(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query1 = f"""
        SELECT CCNum
        FROM UserCard
        WHERE Id = {self.id}
        """
        self.total = 10000
        self.hour = '5'
        lst = list(cursor.execute(query1))
        self.credit_card = lst[0][0]

        self.assertNotEqual(self.credit_card[-1], self.hour)
        self.assertNotEqual(self.credit_card[-1], self.credit_card[0])

    def test(self):
        new_total = fetch_payment_discount(self.credit_card, self.hour, self.total)[1]
        self.assertEqual(new_total, self.total)

    def tearDown(self) -> None:
        self.assertNotEqual(self.credit_card[-1], self.hour)
        self.assertNotEqual(self.credit_card[-1], self.credit_card[0])
