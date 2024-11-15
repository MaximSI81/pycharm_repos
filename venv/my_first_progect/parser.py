from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains, ScrollOrigin
from selenium.webdriver.common.keys import Keys
from random import choice
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, ElementClickInterceptedException, TimeoutException

options = webdriver.ChromeOptions()
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

url = 'https://cosmetic.magnit.ru/?ysclid=m3c21m0r9d638692787'
data = []
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
    browser.execute_script("window.scrollBy(0,5000)")
    wait.until(ec.visibility_of_element_located(('xpath', '//a[@href="/catalog?shopCode=458672"]'))).click()

    while True:
        time.sleep(1)
        try:
            el = wait.until(ec.visibility_of_element_located(('xpath', '//span[text()="Показать ещё"]')))
            el.click()
            ActionChains(browser).move_to_element(el).perform()
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
            print(e)
            break
    for i in browser.find_elements('xpath',
                                   '//div[@class="pl-stack-item pl-stack-item_size-6 pl-stack-item_size-4-m pl-stack-item_size-3-ml unit-catalog__stack-item"]//a'):
        print(i.get_attribute('title'))
