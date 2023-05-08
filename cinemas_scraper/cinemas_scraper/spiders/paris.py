import requests
import scrapy
from scrapy.http import Request
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
from scrapy_splash import SplashRequest 


class IvSpider(scrapy.Spider):
    name = 'paris'
    start_urls = ['https://www.ivi.ru/movies/all']

    def parse(self, response):
        for link in response.css('ul.searchBlock__contentVirtual li.searchResultItem searchBlock__searchResultItem a::attr(href)'):  
            yield response.follow(url=link, callback=self.parse_films)

        #циклы для перебора страниц из поисковика
        # for i in range(1,3):
        #     next_page = f'https://www.ivi.ru/movies/all/page{i}'
        #     yield response.follow(next_page, callback=self.parse)
        # i=1
        # while(i<50):
        #     i=i+1
        #     next_page = f'https://www.ivi.ru/movies/all/page{i}'
        #     yield response.follow(next_page, callback=self.parse)
        
    def parse_films(self, response):
        
        # #условия при наличии определенных классов
        # if response.css("div.purchase-options__actions_buy div.plateTile__caption").get():
        #     cost_fullhd = response.css("div.purchase-options__actions_buy div.plateTile__caption::text").get_first()
        #     yield{
        #         'cost_fullhd':cost_fullhd,
        #     }
        # if response.css("div.nbl-button_style_ran nbl-button_size_shinnok").get():
        #     simple_cost = response.css("div.nbl-button_style_ran nbl-button_size_shinnok::text").get()
        #     yield{
        #         'simple_cost':simple_cost,
        #     }

        yield{
            'name':response.css('div.watchTitle__title::text').get(),
            'languages':response.css('div.watchOptions__values::text').get()
        }
