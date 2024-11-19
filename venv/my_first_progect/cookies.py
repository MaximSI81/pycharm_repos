from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

'''service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

url = 'https://cosmetic.magnit.ru/?ysclid=m3c21m0r9d638692787'
with driver as browser:
    browser.get(url)

    app_location__info = ('xpath', '//div[@class="app-location__info"]/span')
    wait.until(ec.visibility_of_element_located(app_location__info)).click()

    placeholder = ('xpath', '//input[@placeholder="Найти магазин по адресу"]')
    wait.until(ec.visibility_of_element_located(placeholder)).send_keys('Лыткарино')
    enter_address = ('xpath', '//p[text()="Московская область, г. Лыткарино, мкр. 6-й, д. 15Б, помещ 1"]')
    wait.until(ec.visibility_of_element_located(enter_address)).click()
    button_choose = ('xpath', '//button[text()="Выбрать"]')
    wait.until(ec.visibility_of_element_located(button_choose)).click()
    print(browser.get_cookies())'''

cookies = [
    {'domain': '.magnit.ru', 'expiry': 1766608524, 'httpOnly': False, 'name': 'KFP_DID', 'path': '/', 'sameSite': 'Lax',
     'secure': True, 'value': 'c32874e5-90a0-e21d-7fb4-7d70cc4fa8a8'},
    {'domain': 'cosmetic.magnit.ru', 'expiry': 1763605480, 'httpOnly': False, 'name': 'shopCode', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': '458672'},
    {'domain': '.magnit.ru', 'expiry': 1739932526, 'httpOnly': False, 'name': 'oxxfgh', 'path': '/', 'sameSite': 'Lax',
     'secure': True, 'value': 'b909431a-6350-49b5-b98f-f1831281f224#0#7884000000#5000#1800000#12840'},
    {'domain': '.magnit.ru', 'expiry': 1763584521, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'sameSite': 'None',
     'secure': True, 'value': '1732048522'},
    {'domain': '.magnit.ru', 'expiry': 1732050322, 'httpOnly': False, 'name': '_ym_visorc', 'path': '/',
     'sameSite': 'None', 'secure': True, 'value': 'b'},
    {'domain': 'cosmetic.magnit.ru', 'httpOnly': False, 'name': 'mg_udi', 'path': '/', 'sameSite': 'Lax',
     'secure': False, 'value': 'B754AD15-8592-784D-268F-F0E662AEB7BF'},
    {'domain': 'cosmetic.magnit.ru', 'expiry': 1763605480, 'httpOnly': False, 'name': 'nmg_sp', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'Y'},
    {'domain': 'cosmetic.magnit.ru', 'expiry': 1763605480, 'httpOnly': False, 'name': 'nmg_cty', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': '%D0%9B%D1%8B%D1%82%D0%BA%D0%B0%D1%80%D0%B8%D0%BD%D0%BE'},
    {'domain': '.magnit.ru', 'expiry': 1766608528, 'httpOnly': False, 'name': '_ga_MRRD7S5PSR', 'path': '/',
     'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1732048521.1.0.1732048528.0.0.0'},
    {'domain': '.magnit.ru', 'expiry': 1763605472, 'httpOnly': True, 'name': 'mg_at', 'path': '/', 'sameSite': 'Strict',
     'secure': True, 'value': '%7B%7D'},
    {'domain': '.magnit.ru', 'expiry': 1766608521, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax',
     'secure': False, 'value': 'GA1.1.1323794321.1732048522'},
    {'domain': '.magnit.ru', 'expiry': 1732120522, 'httpOnly': False, 'name': '_ym_isad', 'path': '/',
     'sameSite': 'None', 'secure': True, 'value': '2'},
    {'domain': '.magnit.ru', 'expiry': 1763584521, 'httpOnly': False, 'name': '_ym_uid', 'path': '/',
     'sameSite': 'None', 'secure': True, 'value': '1732048522468289660'}]

'''
    app_location__info = ('xpath', '//div[@class="app-location__info"]/span')
    wait.until(ec.visibility_of_element_located(app_location__info)).click()

    placeholder = ('xpath', '//input[@placeholder="Найти магазин по адресу"]')
    wait.until(ec.visibility_of_element_located(placeholder)).send_keys('Лыткарино')
    enter_address = ('xpath', '//p[text()="Московская область, г. Лыткарино, мкр. 6-й, д. 15Б, помещ 1"]')
    wait.until(ec.visibility_of_element_located(enter_address)).click()
    button_choose = ('xpath', '//button[text()="Выбрать"]')
    wait.until(ec.visibility_of_element_located(button_choose)).click()'''
