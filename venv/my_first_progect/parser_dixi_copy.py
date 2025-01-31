import aiohttp
import asyncio
import json
import requests
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException


class ParserDixi:
    def __init__(self):
        self.headers = {'User-Agent': UserAgent().random}
        self.data = []

    def pars(self, link):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        with driver as browser:
            browser.implicitly_wait(5)
            browser.get(link)
            with open('cookies_dixi.json', 'r') as file:
                cookies = json.load(file)
                for cookie in cookies:
                    browser.add_cookie(cookie)
            browser.refresh()
            browser.maximize_window()
            while True:
                try:
                    browser.find_element(By.XPATH, "//button[@class='btn grey more-orders']").click()
                except ElementNotInteractableException:
                    break
            html = browser.page_source
            if html:
                soup = BeautifulSoup(html, 'lxml')

                for t in soup.find_all('article', class_='card bs-state'):
                    if t.find('h3'):
                        try:
                            print(t.find('h3', class_='card__title').text, '------',
                                  t.find('div', class_='card__price-num').text)
                        except AttributeError:
                            pass


prod = ['molochnye-produkty-yaytsa/', 'myaso-ptitsa/', 'myasnaya-gastronomiya/', 'ovoshchi-frukty/',
        'konditerskie-izdeliya-torty/', 'chay-kofe-kakao/']
url = 'https://dixy.ru/catalog/molochnye-produkty-yaytsa/'

PD = ParserDixi()
x = 0
for i in range(len(prod)):
    try:
        PD.pars(f'https://dixy.ru/catalog/{prod[i - x]}')
    except ElementClickInterceptedException:
        x += 1
        continue
