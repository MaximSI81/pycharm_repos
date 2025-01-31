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
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, \
    ElementClickInterceptedException, TimeoutException
from magnit_selenium import cookies

options = webdriver.ChromeOptions()
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

url = 'https://cosmetic.magnit.ru/?ysclid=m3c21m0r9d638692787'
data = []
with driver as browser:
    browser.get(url)
    browser.maximize_window()
    browser.delete_all_cookies()
    for c in cookies:
        browser.add_cookie(c)
    browser.refresh()

    browser.execute_script("window.scrollBy(0,5000)")
    wait.until(ec.visibility_of_element_located(('xpath', '//a[@href="/catalog?shopCode=458672"]'))).click()

    while True:
        selector_name = ('xpath', '//div[@class="pl-text unit-catalog-product-preview-title"]')
        selector_price = ('xpath', '//span[@class="pl-text unit-catalog-product-preview-prices__regular"]/span')
        time.sleep(1)
        try:
            el = wait.until(ec.visibility_of_element_located(('xpath', '//span[text()="Показать ещё"]')))
            el.click()
            ActionChains(browser).move_to_element(el).perform()
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
            print(e)
            break

    for n, p in zip(browser.find_elements(*selector_name), browser.find_elements(*selector_price)):
        print(f'{n.text} --- {p.text}')
