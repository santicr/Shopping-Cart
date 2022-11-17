from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import unittest, psycopg2
import time

chromedriver_autoinstaller.install()

def exist_user(user_name: str, password: str):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    SELECT * FROM
    user_web
    WHERE
    name = '{user_name}' AND
    password = '{password}'
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    res = len(cursor.fetchall())
    cursor.close()
    conn.close()
    return res

def verify_card(data):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    SELECT balance FROM
    usercard
    WHERE
    name = '{data[0]}' AND
    lastname1 = '{data[1]}' AND
    lastname2 = '{data[2]}' AND
    ccnum = '{data[3]}' AND
    ccv = '{data[4]}'
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res

def verify_cart_items(user_name):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    SELECT itemid, quantity FROM
    cart
    WHERE
    user_web = '{user_name}'
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    res = cursor.fetchall()
    flag1 = len(res)
    flag2 = True
    for row in res:
        itemid = row[0]
        quant = row[1]
        query2 = f"""
        select quantity
        from item
        where id = {itemid}
        """
        cursor.execute(query2)
        quant_item = cursor.fetchone()[0]
        if quant > quant_item:
            flag2 = False
    cursor.close()
    conn.close()
    return flag1 and flag2

    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    SELECT balance FROM
    usercard
    WHERE
    name = '{data[0]}' AND
    lastname1 = '{data[1]}' AND
    lastname2 = '{data[2]}' AND
    ccnum = {data[3]} AND
    ccv = {data[4]}
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    res = len(cursor.fetchall())
    cursor.close()
    conn.close()
    return res

def get_amount(user_name):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = """
    SELECT sum(cart.quantity * price) FROM
    cart INNER JOIN item ON(itemid = id)
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    total = cursor.fetchone()
    if len(total):
        total = total[0]
    else:
        total = -1
    return total

def get_items_quant(user_name):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    select itemid, item.quantity - cart.quantity from
    cart INNER JOIN item ON(itemid = id)
    where user_web = '{user_name}'
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

def get_items_quant_2(user_name):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    query1 = f"""
    select itemid, item.quantity from
    cart INNER JOIN item ON(itemid = id)
    where user_web = '{user_name}'
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

def verify_new_items_quant(data):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    ans = True
    for itemid, quant in data:
        query1 = f"""
        select quantity
        from item
        where id = {itemid}
        """
        cursor.execute(query1)
        new_quant = cursor.fetchone()[0]
        if new_quant != quant:
            ans = False
    cursor.close()
    conn.close()
    return ans

def pre_process():
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()
    # Focus function, move through element
    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys("santicr21")

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("Prueba1234@")

    # Add to cart process
    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    add_but = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div > div > div > form > button")
    add_but.click()

    driver.quit()

def pre_process_3(user):
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()
    # Focus function, move through element
    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys(user)

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("Prueba1234@")

    # Add to cart process
    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    add_but = driver.find_element(by=By.CSS_SELECTOR, value="body > div > div > div > div > form > button")
    add_but.click()

    driver.quit()

def test_process(data, user_name):
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()
    # Focus function, move through element
    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys("santicr21")

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("Prueba1234@")

    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    # Add to cart process
    cart_but = driver.find_element(by=By.CSS_SELECTOR, value='body > nav > div > a:nth-child(5) > img')
    cart_but.click()
    
    total = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h4:nth-child(5)').text
    total = float(total.strip().split()[3])

    pay_but = driver.find_element(by = By.CSS_SELECTOR, value = "body > form:nth-child(9) > button")
    pay_but.click()
    items_list = get_items_quant(user_name)

    # Pay process
    name, lname1, lname2, ccnum, ccv = data
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

    #Get title
    title = driver.find_element(by=By.CSS_SELECTOR, value = 'body > center > h2').text
    driver.quit()
    return items_list, total, title

def test_process_2(data, user_name):
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()
    # Focus function, move through element
    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys(user_name)

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("Prueba1234@")

    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    # Add to cart process
    cart_but = driver.find_element(by=By.CSS_SELECTOR, value='body > nav > div > a:nth-child(5) > img')
    cart_but.click()
    
    total = driver.find_element(by=By.CSS_SELECTOR, value = 'body > h4:nth-child(5)').text
    total = float(total.strip().split()[3])
    time.sleep(2)
    pay_but = driver.find_element(by = By.CSS_SELECTOR, value = "body > form:nth-child(9) > button")
    pay_but.click()
    items_list = get_items_quant_2(user_name)

    # Pay process
    name, lname1, lname2, ccnum, ccv = data
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

    #Get title
    title = driver.find_element(by=By.CSS_SELECTOR, value = 'body > p').text

    driver.quit()
    return items_list, total, title

class Test1(unittest.TestCase):
    def setUp(self) -> None:
        self.user_name = "santicr21"
        self.password = "Prueba1234@"
        self.data = ["Santiago", "Caicedo", "Rojas", "0123456789012344", "783"]
        self.balance = verify_card(self.data)
        pre_process_3("santicr23")
        pre_process_3("santicr23")
        pre_process()
        pre_process()
        pre_process()
        self.exist_card = len(self.balance) if self.balance is not None else 0
        if self.exist_card: self.balance = self.balance[0]
        self.amount = get_amount(self.user_name)

        self.assertEqual(exist_user(self.user_name, self.password), True)
        self.assertEqual(self.exist_card, True)
        self.assertEqual(verify_cart_items(self.user_name), True)
        self.assertLessEqual(self.amount, self.balance)

    def test(self):
        self.items_list, self.amount, self.title = test_process(self.data, self.user_name)
        self.assertEqual(self.title, "Afrodita accesorios")

    def tearDown(self) -> None:
        self.assertEqual(exist_user(self.user_name, self.password), True)
        self.assertEqual(verify_card(self.data)[0], self.balance - self.amount)
        self.assertEqual(verify_new_items_quant(self.items_list), True)
        self.balance = verify_card(self.data)
        self.exist_card = len(self.balance) if self.balance is not None else 0
        self.assertEqual(self.exist_card, True)

class Test2(unittest.TestCase):
    def setUp(self) -> None:
        self.user_name = "santicr21"
        self.password = "Prueba1234@"
        self.data = ["Santiago", "Caicedo", "Rojas", "9123456789012344", "783"]
        self.balance = verify_card(self.data)
        pre_process()
        self.exist_card = len(self.balance) if self.balance is not None else 0
        if self.exist_card: self.balance = self.balance[0]
        self.amount = get_amount(self.user_name)

        self.assertEqual(exist_user(self.user_name, self.password), True)
        self.assertEqual(self.exist_card, False)
        self.assertEqual(verify_cart_items(self.user_name), True)
        self.items_list = []

    def test(self):
        self.items_list, self.amount, self.title = test_process_2(self.data, self.user_name)
        self.assertEqual(self.title, "Datos de tarjeta de crédito no válidas")

    def tearDown(self) -> None:
        self.assertEqual(exist_user(self.user_name, self.password), True)
        self.assertEqual(verify_new_items_quant(self.items_list), True)
        self.balance = verify_card(self.data)
        self.exist_card = len(self.balance) if self.balance is not None else 0
        self.assertEqual(self.exist_card, False)

class Test3(unittest.TestCase):
    def setUp(self) -> None:
        self.user_name = "santicr23"
        self.password = "Prueba1234@"
        self.data = ["Santiago", "Caicedo", "Rojas", "0123456789012344", "783"]
        self.balance = verify_card(self.data)
        self.exist_card = len(self.balance) if self.balance is not None else 0
        if self.exist_card: self.balance = self.balance[0]
        self.amount = get_amount(self.user_name)

        self.assertEqual(exist_user(self.user_name, self.password), True)
        self.assertEqual(self.exist_card, True)
        self.assertEqual(verify_cart_items(self.user_name), False)
        self.items_list = []

    def test(self):
        self.items_list, self.amount, self.title = test_process_2(self.data, self.user_name)
        self.assertEqual(self.title, "Error, la cantidad de los productos a comprar es mayor a la disponible")

    def tearDown(self) -> None:
        self.assertEqual(exist_user(self.user_name, self.password), True)
        self.assertEqual(verify_new_items_quant(self.items_list), True)
        self.balance = verify_card(self.data)
        self.exist_card = len(self.balance) if self.balance is not None else 0
        self.assertEqual(self.exist_card, True)

class Test4(unittest.TestCase):
    def setUp(self) -> None:
        self.user_name = "santicr22"
        self.password = "Prueba1234@"
        self.data = ["Santiago", "Caicedo", "Rojas", "1234567890000981", "783"]
        self.balance = verify_card(self.data)
        pre_process_3(self.user_name)
        self.exist_card = len(self.balance) if self.balance is not None else 0
        if self.exist_card: self.balance = self.balance[0]
        self.amount = get_amount(self.user_name)

        self.assertEqual(exist_user(self.user_name, self.password), True)
        self.assertEqual(self.exist_card, True)
        self.assertEqual(verify_cart_items(self.user_name), True)
        self.assertGreater(self.amount, self.balance)

    def test(self):
        self.items_list, self.amount, self.title = test_process_2(self.data, self.user_name)
        self.assertEqual(self.title, "Saldo insuficiente")

    def tearDown(self) -> None:
        self.assertEqual(exist_user(self.user_name, self.password), True)
        self.assertEqual(verify_card(self.data)[0], self.balance)
        self.assertEqual(verify_new_items_quant(self.items_list), True)
        self.balance = verify_card(self.data)
        self.exist_card = len(self.balance) if self.balance is not None else 0
        self.assertEqual(self.exist_card, True)