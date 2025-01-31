from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

service = Service(executable_path=ChromeDriverManager().install())

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
    print(browser.get_cookies())

    app_location__info = ('xpath', '//div[@class="app-location__info"]/span')
    wait.until(ec.visibility_of_element_located(app_location__info)).click()

    placeholder = ('xpath', '//input[@placeholder="Найти магазин по адресу"]')
    wait.until(ec.visibility_of_element_located(placeholder)).send_keys('Лыткарино')
    enter_address = ('xpath', '//p[text()="Московская область, г. Лыткарино, мкр. 6-й, д. 15Б, помещ 1"]')
    wait.until(ec.visibility_of_element_located(enter_address)).click()
    button_choose = ('xpath', '//button[text()="Выбрать"]')
    wait.until(ec.visibility_of_element_located(button_choose)).click()
