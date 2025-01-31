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
from selenium.webdriver.support.ui import WebDriverWait


class ParserMagnit:
    def __init__(self, prod, tags):

        self.prod = prod
        self.tags = tags
        self.headers = {'User-Agent': UserAgent().random}

    def pars(self, link):
        options = webdriver.ChromeOptions()
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        with driver as browser:
            browser.implicitly_wait(5)
            browser.get(link)
            with open('cookies.json', 'r') as file:
                cookies = json.load(file)
                for cookie in cookies:
                    browser.add_cookie(cookie)
            browser.refresh()
            browser.maximize_window()
            time.sleep(5)
            html = browser.page_source
            if html:
                soup = BeautifulSoup(html, 'lxml')

                for t in soup.find_all('div', class_=self.tags[0]):
                    if t.find('a'):
                        try:
                            print(t.find('a')['title'], '------',
                                  t.find('span', class_=self.tags[1]).text)
                        except AttributeError:
                            pass


prod = ['молоко', 'колбаса', 'кофе']
tags = [
    'pl-stack-item pl-stack-item_size-6 pl-stack-item_size-6-s pl-stack-item_size-4-m pl-stack-item_size-3-ml pl-stack-item_size-2-xl unit-catalog__stack-item',
    'pl-text unit-catalog-product-preview-prices__regular']

p = ParserMagnit(prod, tags)

#p.pars('https://magnit.ru/search?term=молоко')
