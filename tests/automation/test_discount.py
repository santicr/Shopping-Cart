from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import unittest, psycopg2
import sys
import time
from datetime import datetime
sys.path.append('/Users/santicr/Desktop/Github/Shopping-Cart/controller')
from controller_pay import fetch_payment_discount

chromedriver_autoinstaller.install()

def fetch_credit_card(id):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    select * from usercard
    where id = {id}
    """
    cursor.execute(query1)
    lst = cursor.fetchone()
    cursor.close()
    conn.close()
    return lst

def verify_card(data):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    SELECT * FROM usercard
    WHERE
    name = '{data[1]}' AND
    lastname1 = '{data[2]}' AND
    lastname2 = '{data[3]}' AND
    ccnum = '{data[4]}' AND
    ccv = '{data[5]}'
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    flag = len(cursor.fetchall())
    cursor.close()
    conn.close()
    print(flag)
    return flag

def process_test_1(data):
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()

    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    time.sleep(2)

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys("santicr21")

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("Prueba1234@")

    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    time.sleep(2)
    
    # Add to cart process
    add_but = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div > div > div > form > button")
    add_but.click()

    time.sleep(2)

    cart_but = driver.find_element(by=By.CSS_SELECTOR, value='body > nav > div > a:nth-child(5) > img')
    cart_but.click()
    
    total = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h4:nth-child(5)').text
    total = float(total.strip().split()[3])

    time.sleep(2)

    pay_but = driver.find_element(by = By.CSS_SELECTOR, value = "body > form:nth-child(9) > button")
    pay_but.click()

    time.sleep(1)

    #Pay process
    id, name, lname1, lname2, ccnum, ccv, balance = data
    cc_name = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(1) > input')
    cc_name.click()
    cc_name.send_keys(name)

    cc_lname1 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(2) > input')
    cc_lname1.click()
    cc_lname1.send_keys(lname1)

    cc_lname2 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(3) > input')
    cc_lname2.click()
    cc_lname2.send_keys(lname2)

    cc_num = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(4) > input')
    cc_num.click()
    cc_num.send_keys(ccnum)

    cc_ccv = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(5) > input')
    cc_ccv.click()
    cc_ccv.send_keys(ccv)

    pay_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    pay_but.click()

    time.sleep(2)

    # Get discount and back to main process
    discount = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h3').text
    main = driver.find_element(by=By.CSS_SELECTOR, value = 'body > a')
    main.click()

    driver.quit()

    return total - float(discount)

def process_test_2(data):
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()

    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    time.sleep(2)

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys("santicr21")

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("Prueba1234@")

    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    time.sleep(2)
    
    # Add to cart process
    add_but = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div > div > div > form > button")
    add_but.click()

    time.sleep(2)

    cart_but = driver.find_element(by=By.CSS_SELECTOR, value='body > nav > div > a:nth-child(5) > img')
    cart_but.click()
    
    total = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h4:nth-child(5)').text
    total = float(total.strip().split()[3])

    time.sleep(2)

    pay_but = driver.find_element(by = By.CSS_SELECTOR, value = "body > form:nth-child(9) > button")
    pay_but.click()

    time.sleep(1)

    #Pay process
    id, name, lname1, lname2, ccnum, ccv, balance = data
    cc_name = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(1) > input')
    cc_name.click()
    cc_name.send_keys(name)

    cc_lname1 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(2) > input')
    cc_lname1.click()
    cc_lname1.send_keys(lname1)

    cc_lname2 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(3) > input')
    cc_lname2.click()
    cc_lname2.send_keys(lname2)

    cc_num = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(4) > input')
    cc_num.click()
    cc_num.send_keys(ccnum)

    cc_ccv = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(5) > input')
    cc_ccv.click()
    cc_ccv.send_keys(ccv)

    pay_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    pay_but.click()

    time.sleep(2)

    # Get discount and back to main process
    discount = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h3').text
    main = driver.find_element(by=By.CSS_SELECTOR, value = 'body > a')
    main.click()

    driver.quit()

    return total, total - float(discount)

def process_test_3(data):
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()

    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    time.sleep(2)

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys("santicr21")

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("Prueba1234@")

    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    time.sleep(2)
    
    # Add to cart process
    add_but = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div > div > div > form > button")
    add_but.click()

    time.sleep(2)

    cart_but = driver.find_element(by=By.CSS_SELECTOR, value='body > nav > div > a:nth-child(5) > img')
    cart_but.click()
    
    total = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h4:nth-child(5)').text
    total = float(total.strip().split()[3])

    time.sleep(2)

    pay_but = driver.find_element(by = By.CSS_SELECTOR, value = "body > form:nth-child(9) > button")
    pay_but.click()

    time.sleep(1)

    #Pay process
    id, name, lname1, lname2, ccnum, ccv, balance = data
    cc_name = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(1) > input')
    cc_name.click()
    cc_name.send_keys(name)

    cc_lname1 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(2) > input')
    cc_lname1.click()
    cc_lname1.send_keys(lname1)

    cc_lname2 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(3) > input')
    cc_lname2.click()
    cc_lname2.send_keys(lname2)

    cc_num = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(4) > input')
    cc_num.click()
    cc_num.send_keys(ccnum)

    cc_ccv = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(5) > input')
    cc_ccv.click()
    cc_ccv.send_keys(ccv)

    pay_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    pay_but.click()

    time.sleep(2)

    # Get discount and back to main process
    discount = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h3').text
    main = driver.find_element(by=By.CSS_SELECTOR, value = 'body > a')
    main.click()

    driver.quit()

    return total, total - float(discount)

def process_test_4(data):
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()

    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    time.sleep(2)

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys("santicr21")

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("Prueba1234@")

    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    time.sleep(2)
    
    # Add to cart process
    add_but = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div > div > div > form > button")
    add_but.click()

    time.sleep(2)

    cart_but = driver.find_element(by=By.CSS_SELECTOR, value='body > nav > div > a:nth-child(5) > img')
    cart_but.click()
    
    total = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h4:nth-child(5)').text
    total = float(total.strip().split()[3])

    time.sleep(2)

    pay_but = driver.find_element(by = By.CSS_SELECTOR, value = "body > form:nth-child(9) > button")
    pay_but.click()

    time.sleep(1)

    #Pay process
    id, name, lname1, lname2, ccnum, ccv, balance = data
    cc_name = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(1) > input')
    cc_name.click()
    cc_name.send_keys(name)

    cc_lname1 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(2) > input')
    cc_lname1.click()
    cc_lname1.send_keys(lname1)

    cc_lname2 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(3) > input')
    cc_lname2.click()
    cc_lname2.send_keys(lname2)

    cc_num = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(4) > input')
    cc_num.click()
    cc_num.send_keys(ccnum)

    cc_ccv = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(5) > input')
    cc_ccv.click()
    cc_ccv.send_keys(ccv)

    pay_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    pay_but.click()

    driver.quit()

    return total

class Test1(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 4
        self.hour = str(int(datetime.now().hour) - 12)
        self.data = fetch_credit_card(self.id)
        self.credit_card = self.data[4]
        self.total = process_test_1(self.data)

        self.assertEqual(verify_card(self.data), 1)
        self.assertEqual(self.hour, self.credit_card[-1])
        self.assertLessEqual(int(self.credit_card[0]) + int(self.credit_card[1]), 4)

    def test(self):
        self.new_total = fetch_payment_discount(self.credit_card, self.hour, self.total)[1]
        self.assertEqual(self.new_total, self.total - (self.total * int(self.hour) / 100))
    
    def tearDown(self) -> None:
        self.assertEqual(verify_card(self.data), 1)
        self.assertEqual(self.hour, self.credit_card[-1])
        self.assertLessEqual(int(self.credit_card[0]) + int(self.credit_card[1]), 4)
        self.assertLess(self.new_total, self.total)

class Test2(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 3
        self.data = fetch_credit_card(self.id)
        self.credit_card = self.data[4]
        self.hour = str(int(datetime.now().hour) - 12)

        self.assertEqual(verify_card(self.data), 1)
        self.assertNotEqual(self.hour, self.credit_card[-1])
        self.assertGreater(int(self.credit_card[0]) + int(self.credit_card[-1]), 4)

    def test(self):
        self.total, new_total = process_test_2(self.data)
        self.assertEqual(new_total, self.total - (self.total * 0.08))

    def tearDown(self) -> None:
        self.assertEqual(verify_card(self.data), 1)
        self.assertNotEqual(self.hour, self.credit_card[-1])
        self.assertGreater(int(self.credit_card[0]) + int(self.credit_card[-1]), 4)

class Test3(unittest.TestCase):
    def setUp(self) -> None:
        self.id = 2
        self.data = fetch_credit_card(self.id)
        self.credit_card = self.data[4]
        self.hour = str(int(datetime.now().hour) - 12)

        self.assertEqual(verify_card(self.data), 1)
        self.assertEqual(self.hour, self.credit_card[-1])
        self.assertGreater(int(self.credit_card[0]) + int(self.credit_card[-1]), 4)
    
    def test(self):
        self.total, new_total = process_test_3(self.data)
        fp = self.total - (self.total * (int(self.hour) / 100))
        self.assertEqual(new_total, fp - fp * 0.08)
    
    def tearDown(self) -> None:
        self.assertEqual(verify_card(self.data), 1)
        self.assertEqual(self.hour, self.credit_card[-1])
        self.assertGreater(int(self.credit_card[0]) + int(self.credit_card[-1]), 4)

class Test4(unittest.TestCase):
    def setUp(self) -> None:
        self.hour = str(int(datetime.now().hour) - 12)
        self.data = fetch_credit_card(1)
        self.credit_card = self.data[4]

        self.assertEqual(verify_card(self.data), 1)
        self.assertNotEqual(self.credit_card[-1], self.hour)
        self.assertNotEqual(self.credit_card[-1], self.credit_card[0])

    def test(self):
        self.total = process_test_4(self.data)
        new_total = fetch_payment_discount(self.credit_card, self.hour, self.total)[1]
        self.assertEqual(new_total, self.total)

    def tearDown(self) -> None:
        self.assertEqual(verify_card(self.data), 1)
        self.assertNotEqual(self.credit_card[-1], self.hour)
        self.assertNotEqual(self.credit_card[-1], self.credit_card[0])