from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import unittest, time, psycopg2

chromedriver_autoinstaller.install()

def get_items_length():
    conn = psycopg2.connect(
        user =  'postgres',
        password = 'admin',
        host = 'localhost',
        database = 'items_db'
    )
    query1 = """
    SELECT * FROM item
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    length = len(cursor.fetchall())
    cursor.close()
    conn.close()
    return length

def test_process(name, quantity, price, description, err):
    driver = Chrome()
    driver.get('http://127.0.0.1:5000/')
    driver.maximize_window()
    text = 'success'

    # Login process
    login = driver.find_element(by=By.CSS_SELECTOR, value="body > nav > div > a:nth-child(2) > button")
    login.click()

    name_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(1) > input")
    name_input.click()
    name_input.send_keys("admin")

    pass_input = driver.find_element(by=By.CSS_SELECTOR, value ="body > div > div > div > form > div:nth-child(2) > input")
    pass_input.click()
    pass_input.send_keys("admin")

    time.sleep(1)

    login_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    login_but.click()

    # Adding process
    add_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > nav > div > form:nth-child(3) > button')
    add_but.click()

    input_name = driver.find_element(by=By.CSS_SELECTOR, value='body > div > div > div > form > div:nth-child(1) > input')
    input_name.click()
    input_name.send_keys(name)

    input_quant = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(2) > input')
    input_quant.click()
    input_quant.send_keys(quantity)

    input_price = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(3) > input')
    input_price.click()
    input_price.send_keys(price)

    input_desc = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div:nth-child(4) > input')
    input_desc.click()
    input_desc.send_keys(description)

    driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > input[type=file]').send_keys('/Users/santicr/Desktop/Accesorios/aretes.jpeg')
    add_but2 = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    
    time.sleep(1)
    
    add_but2.click()

    # Get error and get back to index process
    if err:
        text = driver.find_element(by=By.CSS_SELECTOR, value = 'body > p').text
        time.sleep(1)
        driver.find_element(by=By.CSS_SELECTOR, value = 'body > a').click()
    driver.quit()
    
    return text

class Test1(unittest.TestCase):
    def setUp(self) -> None:
        self.items_length = get_items_length()
        self.product_name = "cade"
        self.quantity = 30
        self.price = 10000
        self.description = "Aretes finos hechos con perlas reales extraídas de lo más profundo del mar"

        self.assertLess(len(self.product_name), 5)
    
    def test(self):
        ans = test_process(self.product_name, self.quantity, self.price, self.description, 1)
        self.assertEqual(ans, "El nombre del producto no cumple con los caracteres minimos")

    def tearDown(self) -> None:
        self.assertLess(len(self.product_name), 5)
        self.assertEqual(self.items_length, get_items_length())

class Test2(unittest.TestCase):
    def setUp(self) -> None:
        self.items_length = get_items_length()
        self.product_name = "Aretes de perlas"
        self.quantity = 0
        self.price = 10000
        self.description = "Aretes finos hechos con perlas reales extraídas de lo más profundo del mar"

        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertLessEqual(self.quantity, 0)
    
    def test(self):
        ans = test_process(self.product_name, self.quantity, self.price, self.description, 1)
        self.assertEqual(ans, "La cantidad del producto no es válida")

    def tearDown(self) -> None:
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertLessEqual(self.quantity, 0)
        self.assertEqual(self.items_length, get_items_length())

class Test3(unittest.TestCase):
    def setUp(self) -> None:
        self.items_length = get_items_length()
        self.product_name = "Aretes de perlas"
        self.quantity = 30
        self.price = 478
        self.description = "Aretes finos hechos con perlas reales extraídas de lo más profundo del mar"

        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quantity, 0)
        self.assertLess(self.price, 500)
    
    def test(self):
        ans = test_process(self.product_name, self.quantity, self.price, self.description, 1)
        self.assertEqual(ans, "El precio no es válido, debe ser mayor o igual a 500 pesos")

    def tearDown(self) -> None:
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quantity, 0)
        self.assertLess(self.price, 500)
        self.assertEqual(self.items_length, get_items_length())

class Test4(unittest.TestCase):
    def setUp(self) -> None:
        self.items_length = get_items_length()
        self.product_name = "Aretes de perlas"
        self.quantity = 30
        self.price = 10000
        self.description = "Are"

        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quantity, 0)
        self.assertGreaterEqual(self.price, 500)
        self.assertLess(len(self.description), 5)
    
    def test(self):
        ans = test_process(self.product_name, self.quantity, self.price, self.description, 1)
        self.assertEqual(ans, "La descripción es muy corta")

    def tearDown(self) -> None:
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quantity, 0)
        self.assertGreaterEqual(self.price, 500)
        self.assertLess(len(self.description), 5)
        self.assertEqual(self.items_length, get_items_length())

class Test5(unittest.TestCase):
    def setUp(self) -> None:
        self.items_length = get_items_length()
        self.product_name = "Aretes de perlas"
        self.quantity = 30
        self.price = 10000
        self.description = "Aretes finos hechos con perlas reales extraídas de lo más profundo del oceano."

        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quantity, 0)
        self.assertGreaterEqual(self.price, 500)
        self.assertGreaterEqual(len(self.description), 5)
    
    def test(self):
        ans = test_process(self.product_name, self.quantity, self.price, self.description, 0)
        self.assertEqual(ans, "success")

    def tearDown(self) -> None:
        self.assertGreaterEqual(len(self.product_name), 5)
        self.assertGreater(self.quantity, 0)
        self.assertGreaterEqual(self.price, 500)
        self.assertGreaterEqual(len(self.description), 5)
        self.assertEqual(self.items_length + 1, get_items_length())