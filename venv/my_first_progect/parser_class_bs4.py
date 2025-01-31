import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
import csv
import random
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector


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
        proxy = random.choice(
            ['socks5h://hZdSqH:0SCocw@188.130.203.29:8000', 'socks5h://cLaFFB:JgGmZC@196.18.12.18:8000',
             'socks5h://cLaFFB:JgGmZC@196.18.15.117:8000'])
        proxies = {'http': proxy, 'https': proxy}
        session = requests.Session()
        #session.proxies.update(proxies)
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
                                        self.products.append(l)

    @staticmethod
    def get_trademark(firm, title):
        if firm in title:
            return True
        return False

    async def main(self):
        tasks = []
        connect = ChainProxyConnector.from_urls(
            ['socks5://hZdSqH:0SCocw@188.130.203.29:8000', 'socks5://cLaFFB:JgGmZC@196.18.12.18:8000',
             'socks5://cLaFFB:JgGmZC@196.18.15.117:8000'])
        #timeout = aiohttp.ClientTimeout(total=.5, connect=0.1, sock_connect=0.1, sock_read=0.3)
        async with aiohttp.ClientSession() as session:
            for i in range(1, self.get_pages(self.get_soup(self.url)) + 1):
                task = asyncio.create_task(self.pars(f'{self.url}&page={i}', session))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def __call__(self, *args, **kwargs):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.main())


products = ['17591-sosiski_kolbasy_delikatesy', '4834-moloko_syr_yaytsa', '4884-ovoshchi_frukty',
            '4855-myaso_ptitsa_kolbasy', '5276-chay_kofe_kakao', '5011-sladosti_torty_pirozhnye', '5269-khleb_vypechka_sneki']

for i in products:
    p = ParserProducts(f'https://magnit.ru/catalog/{i}?shopCode=503051&shopType=1')
    p()
    for e, i in enumerate(p.products):
        print(e, '   ', i)
    with open('products_magnit.csv', 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for row in p.products:  # запись строк
            writer.writerow(row)




