import aiohttp
import asyncio
import json
import requests
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (ElementNotInteractableException, ElementClickInterceptedException,
                                        NoSuchElementException)
import csv
import random
from selenium import webdriver
from seleniumwire import webdriver
import pandas as pd


class ParserDixi:
    def __init__(self, url, prod):
        self.headers = {'User-Agent': UserAgent().random}
        self.data = []
        self.prod = prod
        self.url = url
        self.link = []
        self.prod_inf = []
        self.proxy = random.choice(
            ['socks5://hZdSqH:0SCocw@188.130.203.29:8000', 'socks5://cLaFFB:JgGmZC@196.18.12.18:8000',
             'socks5://cLaFFB:JgGmZC@196.18.15.117:8000'])
        self.trademark = ['кофейня на паяхъ', 'Мясницкий ряд', 'Ремит', 'Мираторг',
                          'Простоквашино', 'Домик в деревне', 'Село Зеленое', 'Красный Октябрь',
                          'РотФронт', 'Яшкино', 'Хлебный Дом', 'Брест-Литовск', 'Добрый'
                          ]

    @staticmethod
    def get_trademark(firm, title):
        if firm in title:
            return True
        return False

    def pars(self, link):
        proxi_options = {
            "proxy": {
                'http': self.proxy,
                'https': self.proxy
            },
        }
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        service = Service(executable_path=ChromeDriverManager().install())
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=proxi_options)
        driver.implicitly_wait(5)
        with driver as browser:
            browser.get(link)
            time.sleep(15)
            with open('cookies_dixi.json', 'r') as file:
                cookies = json.load(file)
                for cookie in cookies:
                    browser.add_cookie(cookie)
            browser.refresh()
            browser.maximize_window()
            while True:
                try:
                    browser.find_element(By.XPATH, "//button[@class='btn grey more-orders']").click()
                except (ElementNotInteractableException, NoSuchElementException):
                    break
            html = browser.page_source
            if html:
                soup = BeautifulSoup(html, 'lxml')
                for t in soup.find_all('article', class_='card bs-state'):
                    if t.find('a'):
                        try:
                            for firm in self.trademark:
                                if self.get_trademark(firm, t.find('h3').text):
                                    self.data.append(t.find('a')['href'])
                                    print(t.find('a')['href'])
                        except AttributeError:
                            pass

    def get_link(self):
        x = -1
        while x < len(self.prod) - 1:
            x += 1
            try:
                print(self.url + self.prod[x])
                self.pars(self.url + self.prod[x])
                self.link += self.data
                print(x)
                print(len(self.link))
            except ElementClickInterceptedException:
                x -= 1
                print(len(self.link))

    def get_prod(self):
        dict_name_column = {'Тип товара': 'Тип продукта',  'Торговая марка': 'Бренд'}
        self.get_link()
        session = requests.Session()
        for l in self.link:
            with session.get(self.url + l[9:], headers=self.headers,
                             proxies={'https': self.proxy}) as responce:
                if responce:
                    soup = BeautifulSoup(responce.text, 'lxml')
                    title = soup.find('h1').text
                    product_information = soup.find_all('div', class_='list__line')
                    l = []
                    price = soup.find('div', class_='card__price-num')
                    for i in product_information:
                        if i.find('span', class_='text').text in (
                                'Тип товара', 'Торговая марка'):
                            if i.find('a'):
                                l.append(
                                    dict_name_column[i.find('span', class_='text').text] + ' ' + i.find('a').find('span').text)
                            else:
                                l.append(i.find('span', class_='text').text + ' ' + 'None')
                    l.append('price' + ' ' + price.text)
                    l.append('date_price' + ' ' + str(pd.to_datetime('today').normalize()))
                    self.prod_inf.append(l)


# асинхронный проход ссылок - не корректно работает
'''
    async def add_list_name_product(self, session, link):
        async with session.get(link) as response:
            print(link)
            if response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                tag_t = soup.find('h1')
                if tag_t:
                    title = tag_t.text
                else:
                    title = 'None'
                print(title)
                product_information = soup.find_all('div', class_='list__line')
                if title != 'Сайт находится на техническом обслуживании' or title is not None:
                    self.prod_inf.append('title' + ' ' + title)
                    price = soup.find('div', class_='card__price-num')
                    if price:
                        self.prod_inf.append('price' + ' ' + price.text)
                    for i in product_information:
                        self.prod_inf.append('title' + ' ' + title)
                        if i.find('span', class_='text').text in (
                                'Торговая марка', 'Страна', 'Тип товара', 'Вид мяса', 'Вес', 'Вкус', 'Часть туши',
                                'Вид овощей', 'Сорт', 'Тип упаковки', 'Срок хранения', 'Категория', 'Цвет', 'Жирность',
                                'Сорт колбасы', 'Фасовка', 'Способ обработки', 'Вид кофе', 'Сорт зерна', 'Вид чая',
                                'Сорт чая', 'Ароматизатор'):
                            if i.find('a'):
                                self.prod_inf.append(
                                    i.find('span', class_='text').text + ' ' + i.find('a').find('span').text)
                            else:
                                self.prod_inf.append(i.find('span', class_='text').text + ' ' + 'None')


    async def main(self):
        tasks = []
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for l in self.link:
                task = asyncio.create_task(self.add_list_name_product(session, self.url + l[9:]))
                tasks.append(task)
            await asyncio.gather(*tasks)


    def __call__(self, *args, **kwargs):
        self.get_link()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.main())
'''
prod = ['molochnye-produkty-yaytsa/', 'konditerskie-izdeliya-torty/', 'ovoshchi-frukty/', 'khleb-i-vypechka/', 'myaso-ptitsa/', 'myasnaya-gastronomiya/', 'chay-kofe-kakao/']
url = 'https://dixy.ru/catalog/'

data = []

for p in prod:
    PD = ParserDixi(url, [p])
    PD.get_prod()
    data += PD.prod_inf
with open('products.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for row in data:  # запись строк
        writer.writerow(row)


# Здесь происходит вход в систему для получения cookie
'''driver.get('https://dixy.ru/')
driver = webdriver.Chrome()
time.sleep(15) #вводим адрес магазина
cookies = driver.get_cookies()
with open('cookies_dixi.json', 'w') as file:
    json.dump(cookies, file)

with open('cookies_dixi.json', 'r') as file:
    cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
driver.refresh()
time.sleep(5)'''

'''with open('cookies_dixi.json', 'r') as f:
    cookies = json.load(f)[0]
for i, j in cookies.items():
        cookies[i] = str(j)

r = requests.get(url, headers={'User-Agent': UserAgent().random}, cookies=cookies)
s = BeautifulSoup(r.text, 'lxml')
tag = s.find('span', class_='address__text')
print(tag.text)
'''

# проверка прокси
'''proxy_list = ['socks5://hZdSqH:0SCocw@188.130.203.29:8000', 'socks5://cLaFFB:JgGmZC@196.18.12.18:8000',
              'socks5://cLaFFB:JgGmZC@196.18.15.117:8000']

for PROXY in proxy_list:
    proxy_option = {
        "proxy": {
            'http': PROXY,
            'https': PROXY
        }
    }
    try:
        options = webdriver.ChromeOptions()

        url = 'https://2ip.ru/'
        options.page_load_strategy = 'eager'
        #options.add_argument({'User-Agent': UserAgent().random})
        service = Service(executable_path=ChromeDriverManager().install())
        with webdriver.Chrome(options=options, seleniumwire_options=proxy_option,
                              service=service) as browser:
            browser.get(url)
            print(browser.find_element(By.ID, 'd_clip_button').find_element(By.TAG_NAME, 'span').text)

            browser.set_page_load_timeout(5)

            proxy_list.remove(PROXY)
    except Exception as _ex:
        print(f"Превышен timeout ожидания для - {PROXY}")
        print(_ex)
        continue
'''
