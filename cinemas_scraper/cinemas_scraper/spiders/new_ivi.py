import json
from bs4 import BeautifulSoup
import requests
import scrapy
from scrapy.http import Request
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
from scrapy_splash import SplashRequest 


# class IvSpider(scrapy.Spider):
#     name = 'new_ivi'
#     start_urls = ['https://www.ivi.ru/movies/all']


#     def start_requests(self):
#         for url in self.start_urls:
#             ua = UserAgent()
#             yield Request(url=url, callback=self.parse, headers={"User-Agent":ua.random})

#     def parse(self, response):
#         #for link in response.css('ul.gallery__list li.gallery__item a::attr(href)'):
          
             
#         yield response.follow('https://www.ivi.ru/watch/145156', callback=self.parse_films)
#         # сохраняем response.text в файл
#         response = requests.get('https://www.ivi.ru/watch/145156')
#         with open('idontknow.html', 'w', encoding='utf-8') as f:
#             f.write(response.text) 
#         #response = requests.get('https://www.ivi.ru/watch/145156')
        

#         #циклы для перебора страниц из поисковика
#         # for i in range(1,3):
#         #     next_page = f'https://www.ivi.ru/movies/all/page{i}'
#         #     yield response.follow(next_page, callback=self.parse)
#         # i=1
#         # while(i<50):
#         #     i=i+1
#         #     next_page = f'https://www.ivi.ru/movies/all/page{i}'
#         #     yield response.follow(next_page, callback=self.parse)
        
#     def parse_films(self, response):
        
#         #условия при наличии определенных классов
#         if response.css("div.purchase-options__actions_buy div.plateTile__caption").get():
#             cost_fullhd = response.css("div.purchase-options__actions_buy div.plateTile__caption::text").get_first()
#             yield{
#                 'cost_fullhd':cost_fullhd,
#             }
#         if response.css("div.nbl-button_style_ran nbl-button_size_shinnok").get():
#             simple_cost = response.css("div.nbl-button_style_ran nbl-button_size_shinnok::text").get()
#             yield{
#                 'simple_cost':simple_cost,
#             }

#         yield{
#             'name':response.css('div.watchTitle__title::text').get(),
#             'languages':response.css('div.watchOptions__values::text').get()
#         }


class IvSpider(scrapy.Spider):
    name = 'new_ivi'
    start_urls = ['https://www.ivi.ru/watch/145156']
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}

    def start_requests(self):
        
        yield Request(url='https://www.ivi.ru/search/?ivi_search=париж%20по', callback=self.parse, headers=self.headers)
        

    def parse(self, response):   
        yield response.follow('https://www.ivi.ru/search/?ivi_search=париж%20по', callback=self.parse_films, headers=self.headers)
        # response = requests.get('https://www.ivi.ru/search/')
        # with open('idontknow.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        # with open('idontknow.html', 'r', encoding='utf-8') as f:
        #     html_parsing = f.read()

        # #не углублялся, но этот кусок находит нужную мне часть кода и и сохраняет его отдельны json файлом
        # soup = BeautifulSoup(html_parsing, 'html.parser')
        # scripts = soup.find_all('script')
        # for script in scripts:
        #     if script.string is not None and 'window.__INITIAL_STATE__ =' in script.string:
        #         json_str = script.string.split('window.__INITIAL_STATE__ =')[1].strip()
        #         script_parsing = json.loads(json_str)
        #         with open('script_parsing.json', 'w', encoding='utf-8') as f:
        #             json.dump(script_parsing, f)

        # #проверяю для себя сохранилось ли
        # with open('script_parsing.json', 'r', encoding='utf-8') as f:
        #     #print(f.read())
        #     data = json.load(f)

        
    def parse_films(self, response): 
        yield{
            'name':response.css('div.watchTitle__title::text').get(),
            'languages':response.css('div.watchOptions__values::text').get()
        }