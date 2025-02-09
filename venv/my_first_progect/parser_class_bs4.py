import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
import csv
import random, pandas
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
import datetime
import pandas as pd
from sqlalchemy import create_engine


class ParserProducts:

    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': UserAgent().random}
        self.products = []
        self.trademark = ['кофейня на паяхъ', 'Мясницкий ряд', 'Ремит', 'Мираторг',
                          'Простоквашино', 'Домик в деревне', 'Село Зеленое', 'Красный Октябрь',
                          'РотФронт', 'Яшкино', 'Хлебный Дом', 'Брест-Литовск', 'Добрый'
                          ]

    @staticmethod
    def get_soup(url):
        print(url)
        session = requests.Session()
        resp = session.get(url=url, headers={'User-Agent': UserAgent().random})
        return BeautifulSoup(resp.text, 'lxml')

    def get_pages(self, soup):
        return int(soup.find_all('span', class_="pl-button__icon")[-2].text)

    async def pars(self, link, session):
        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                                   start_timeout=0.5)
        async with retry_client.get(link) as response:
            if response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                for tag in soup.find_all('div',
                                         class_="pl-stack-item pl-stack-item_size-6 pl-stack-item_size-4-m pl-stack-item_size-3-ml unit-catalog__stack-item"):
                    if tag.find('a'):
                        for firm in self.trademark:
                            if self.get_trademark(firm, tag.find('a')['title']):
                                async with retry_client.get('https://magnit.ru' + tag.find('a')['href']) as resp:
                                    s = BeautifulSoup(await resp.text(), 'lxml')
                                    if s.find('span', class_='pl-text product-details-offer__title'):
                                        l = []
                                        for tags in s.find_all('div',
                                                               class_='product-details-parameters-list__item'):
                                            t = tags.find_all('span', class_='pl-text')
                                            l.append(t[0].text + ' ' + t[1].text)
                                        l.append('Название' + ' ' + s.find('span', itemprop='name').text)
                                        l.append('price' + ' ' + s.find('span',
                                                                        class_='pl-text product-details-price__current').text)
                                        l.append('date_price' + ' ' + str(pd.to_datetime('today').normalize()))
                                        self.products.append(l)

    @staticmethod
    def get_trademark(firm, title):
        if firm in title:
            return True
        return False

    async def main(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i in range(1, self.get_pages(self.get_soup(self.url)) + 1):
                task = asyncio.create_task(self.pars(f'{self.url}&page={i}', session))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def __call__(self, *args, **kwargs):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.main())


'''products = ['17591-sosiski_kolbasy_delikatesy', '4834-moloko_syr_yaytsa', '4884-ovoshchi_frukty',
            '4855-myaso_ptitsa_kolbasy', '5276-chay_kofe_kakao', '5011-sladosti_torty_pirozhnye', '5269-khleb_vypechka_sneki']

data = []
for i in products:
    p = ParserProducts(f'https://magnit.ru/catalog/{i}?shopCode=503051&shopType=1')
    p()
    data += p.products'''
# загрузка в csv
'''with open('products_magnit.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
for row in data:  # запись строк
    writer.writerow(row)
'''


# сразу в Dataframe
def transformation(description_list, name_column):
    data = []
    for i in name_column:
        for j in description_list[0].split(','):
            if i in j:
                data.append(j.replace(i, '').lstrip())
    return data


def parser_m():
    name_column = ['Название', 'Тип продукта', 'Бренд', 'price', 'date_price']
    pro = ['5269-khleb_vypechka_sneki']
    products = ['17591-sosiski_kolbasy_delikatesy', '4834-moloko_syr_yaytsa', '4884-ovoshchi_frukty',
                '4855-myaso_ptitsa_kolbasy', '5276-chay_kofe_kakao', '5011-sladosti_torty_pirozhnye',
                '5269-khleb_vypechka_sneki']
    data = []
    for i in pro:
        p = ParserProducts(f'https://magnit.ru/catalog/{i}?shopCode=503051&shopType=1')
        p()
        data += p.products
        print(p.products)
    df = pd.DataFrame(columns=name_column)
    x = 0
    for i in data:
        data_list = transformation([','.join(i)], name_column)
        if data_list:
            try:
                df.loc[x] = transformation([','.join(i)], name_column)[:-1]
                x += 1
            except ValueError:
                pass
    return df

df = parser_m()
for d in df.to_dict('records'):
    print(d)
engine = create_engine('postgresql://postgres:020217@192.168.1.33:5432/lesson_base')
df.to_sql(
    name="products_magnit",  # имя таблицы
    con=engine,  # движок
    if_exists="append",  # если таблица уже существует, добавляем
    index=False  # без индекса
)
