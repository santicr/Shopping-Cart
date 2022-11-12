from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import unittest, psycopg2, time

chromedriver_autoinstaller.install()

def fetch_reference(ref):
    conn = psycopg2.connect(
        host = "localhost",
        database = "items_db",
        user = 'postgres',
        password = 'admin'
    )
    cursor = conn.cursor()
    query1 = f"""
    select * from bill
    where reference = '{ref}'
    """
    cursor.execute(query1)
    return len(cursor.fetchall())

def test_process(reference, selector):
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

    # Click and input references process
    ref_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > nav > div > ul:nth-child(2) > li > a')
    ref_but.click()

    ref_input = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > div > input')
    ref_input.click()
    ref_input.send_keys(reference)

    search_but = driver.find_element(by=By.CSS_SELECTOR, value = 'body > div > div > div > form > button')
    search_but.click()

    text = driver.find_element(by=By.CSS_SELECTOR, value = selector).text
    
    driver.quit()
    return text

class Test1(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = ""
        self.selector = 'body > p'
        self.assertEqual(self.reference, "")

    def test(self):
        ans = test_process(self.reference, self.selector)
        self.assertEqual(ans, "No ingresaste nada, intenta de nuevo")
    
    def tearDown(self) -> None:
        self.assertEqual(self.reference, "")

class Test2(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = "3ad95419-b72e-4c2a-8f3d-6de8e2f3a9b0"
        self.num_rows = fetch_reference(self.reference)
        self.selector = 'body > p'
        self.assertEqual(self.num_rows, 0)

    def test(self):
        ans = test_process(self.reference, self.selector)
        self.assertEqual(ans, "La referencia no existe, intenta de nuevo")
    
    def tearDown(self) -> None:
        self.num_rows = fetch_reference(self.reference)
        self.assertEqual(self.num_rows, 0)

class Test3(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = "3ad95419-b72e-4c2a-8f3d-6de8e2f3a9b1"
        self.selector = 'body > h4:nth-child(4)'
        self.num_rows = fetch_reference(self.reference)
        self.assertEqual(self.num_rows, 1)

    def test(self):
        ans = test_process(self.reference, self.selector)[0:19]
        self.assertEqual(ans, "Nombre del producto")
    
    def tearDown(self) -> None:
        self.num_rows = fetch_reference(self.reference)
        self.assertEqual(self.num_rows, 1)