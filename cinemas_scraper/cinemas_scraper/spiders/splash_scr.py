import scrapy
from scrapy_splash import SplashRequest 
import requests


# class QuoteSpider(scrapy.Spider):
#     name = 'train'
#     start_urls = [
#     'http://quotes.toscrape.com/'
#     ]

#     def start_requests(self):
#         url = 'https://quotes.toscrape.com/js/'
#         yield SplashRequest(url, callback=self.parse)
        
#     def parse(self, response):
#         title = response.css('title::text').extract()
#         yield {'titletext': title}



# class IvSpider(scrapy.Spider):
#     name = 'ivi2' 
#     # имя паука
#     start_urls = ['https://www.ivi.ru/search/?ivi_search=париж%20по'] 
#     # ссылка для старта
    
#     def start_requests(self):
#         for url in self.start_urls:
#             yield SplashRequest(url, self.parse, args={'wait': 2}) 
#             # отправляем запрос на ссылку с помощью SplashRequest, чтобы получить отрендеренную страницу через Splash
    
#     def parse(self, response):
#         for film in response.css('div.searchBlock__contentVirtual li.searchResultItem a::attr(href)').getall(): 
#             # получаем ссылки на каждый фильм на странице
#             yield SplashRequest(film, self.parse_films, args={'wait': 2}) 
#             # переходим на страницу каждого фильма и вызываем функцию parse_films для парсинга страницы
            
#     def parse_films(self, response):
#         yield{
#             'name':response.css('div.watchTitle__title::text').get(), 
#             # получаем название фильма
#             'languages':response.css('div.watchOptions__values::text').get() 
#             # получаем язык фильма
#         }
#         for div in response.css('div.watchOptions__iconsList div.watchOptions__nbl-textBadge::text'):
#             # перебираем качества фильма
#             yield{
#                 'quality':response.css('div.watchOptions__iconsList::text').get() 
#                 # получаем качество фильма
#             }


class IviSpider(scrapy.Spider):
    name = 'ivi_q'
    allowed_domains = ['ivi.ru']
    start_urls = ['https://www.ivi.ru/search/?ivi_search=париж%20по']

    

    # def parse(self, response):
    #     for film in response.css('li.searchResultItem a::attr(href)').getall(): 
    #         # получаем ссылки на каждый фильм на странице
    #         yield SplashRequest(film, self.parse_films, args={'wait': 2}) 
    #         # переходим на страницу каждого фильма и вызываем функцию parse_films для парсинга страницы

    # def parse_films(self, response):
    #     yield{
    #         'name':response.css('div.watchTitle__title::text').get(), 
    #         # получаем название фильма
    #         'languages':response.css('div.watchOptions__values::text').get() 
    #         # получаем язык фильма
    #     }


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                args={'wait': 0.5})

    def parse(self, response):
        yield {
            'title': response.css('title::text').get()
        }