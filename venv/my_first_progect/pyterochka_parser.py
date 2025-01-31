from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains, ScrollOrigin
from selenium.webdriver.common.keys import Keys
from random import choice
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, \
    ElementClickInterceptedException, TimeoutException

from fake_useragent import UserAgent
import csv

options = webdriver.ChromeOptions()
# options.add_argument(f'--user-agent={UserAgent().random}')
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

url = 'https://5ka.ru/catalog/'
data = []

with driver as browser:
    browser.implicitly_wait(5)
    browser.get(url)
    browser.maximize_window()
