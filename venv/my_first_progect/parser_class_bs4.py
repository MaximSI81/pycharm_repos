import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent


class ParserProducts:

    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': UserAgent().random}

    @staticmethod
    def get_soup(url):
        resp = requests.get(url=url, headers={'User-Agent': UserAgent().random})
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
                        print(tag.find('a')['title'], '------',
                              tag.find('span', class_="pl-text unit-catalog-product-preview-prices__regular").text)

    async def main(self):
        tasks = []
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for i in range(1, self.get_pages(self.get_soup(self.url)) + 1):
                task = asyncio.create_task(self.pars(f'{self.url}&page={i}', session))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def __call__(self, *args, **kwargs):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.main())


url = 'https://magnit.ru/promo-catalog/150-skidkipokarte?shopCode=503051'
p = ParserProducts(url)
p()
