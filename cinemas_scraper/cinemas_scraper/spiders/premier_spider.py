import requests

import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class PremSpider(CrawlSpider):
    name = 'premier'
    start_urls = ['https://premier.one/video/all']

    rules = (
        Rule(LinkExtractor(allow='video')),
        Rule(LinkExtractor(allow='show'), callback='parse_premier')
    )

    def parse_premier(self, response):
        yield{
            'title':response.css('h1.show-promo__title::text').get(),
            'languages':response.css('div.show-guest-block__price-description::text').get().split()[1]
        }
    #     for link in response.css('div.video-list ul. li.video-list__item a::attr(href)'):
    #         yield response.follow(link, callback=self.parse_films)

    #     next_page = f'https://premier.one/video/all'
    #     yield response.follow(next_page, callback=self.parse)
    #     # for i in range(1,3):
    #     #     next_page = f'https://www.ivi.ru/movies/all/page{i}'
    #     #     yield response.follow(next_page, callback=self.parse)
    #     #i=1
    #     # while(i<5):
    #     #     i=i+1
    #     #     next_page = f'https://premier.one/video/all{i}'
    #     #     yield response.follow(next_page, callback=self.parse)
            

            
    # def parse_films(self, response):
    #     yield{
    #         'title':response.css('h1.show-promo__title::text').get(),
    #         'languages':response.css('div.show-guest-block__price-description::text').get().split()[1]
    #     }

