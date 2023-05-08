import scrapy
from scrapy.http import Request
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
from scrapy_splash import SplashRequest 


# class IvSpider(scrapy.Spider):
#     name = 'ivi'
#     start_urls = ['https://www.ivi.ru/search/?ivi_search=париж%20по']

#     def __init__(self):
#         self.driver = webdriver.Chrome()

#     def start_requests(self):
#         for url in self.start_urls:
#             self.driver.get(url)
#             body = self.driver.page_source
#             yield scrapy.Request(url=url, callback=self.parse, body=body)

#     def parse(self, response):
#         for link in Selector(text=response.body).css('ul.searchBlock__contentVirtual li.searchResultItem a::attr(href)'):
#             self.driver.get(link.get())
#             body = self.driver.page_source
#             yield scrapy.Request(url=link.get(), callback=self.parse_films, body=body)

#     def parse_films(self, response):
#         for div in Selector(text=response.body).css('div.watchOptions__iconsList div.watchOptions__nbl-textBadge::text'):
#             yield{
#                 'quality': div.get()
#             }

#     def closed(self, reason):
#         self.driver.quit()



class MySpider(scrapy.Spider):
    name = "ivi_spider"
    allowed_domains = ["www.ivi.ru"]
    start_urls = ['https://www.ivi.ru/search/?ivi_search=париж%20по']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='render.html',
                args={'wait': 0.5},
            )

    def parse(self, response):
        for movie in response.xpath("//div[contains(@class, 'nbl-slimPosterBlock')]"):
            title = movie.xpath(".//a[contains(@class, 'nbl-ellipsis')]/text()") \
                .extract_first()
            yield {'title': title}
















class IvSpider(scrapy.Spider):
    name = 'ivi'
    start_urls = ['https://www.ivi.ru/search/?ivi_search=париж%20по']


    def parse(self, response):
        for link in response.css('li.searchResultItem  a::attr(href)'):
            yield response.follow(link, callback=self.parse_films)
            ua = UserAgent()
            yield scrapy.Request(self.start_urls, callback=self.parse)
            # yield response.follow(link, callback=self.parse_films)
            # ua = UserAgent()
            # yield scrapy.Request(self.start_urls, headers={'User-Agent': ua.random}, callback=self.parse)

    def parse_films(self, response):
        yield{
            'name':response.css('div.watchTitle__title::text').get(),
            'languages':response.css('div.watchOptions__values::text').get()
        }
        # for div in response.css('div.watchOptions__iconsList div.watchOptions__nbl-textBadge::text'):
        #     yield{
        #         'quality':response.css('div.watchOptions__iconsList::text').get()
        #     }