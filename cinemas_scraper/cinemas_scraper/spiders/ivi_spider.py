import scrapy

class IvSpider(scrapy.Spider):
    name = 'ivi'
    start_urls = ['https://www.ivi.ru/movies/all']

    def parse(self, response):
        for link in response.css('ul.gallery__list li.gallery__item a::attr(href)'):
            yield response.follow(link, callback=self.parse_films)

        for i in range(1,3):
            next_page = f'https://www.ivi.ru/movies/all/page{i}'
            yield response.follow(next_page, callback=self.parse)



    def parse_films(self, response):
        yield{
            'qualitys':response.css('div.watchTitle__title::text').get(),
            'languages':response.css('div.watchOptions__values::text').get()
        }