from scrapy import Spider
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

class MySpider(Spider):
    name = 'myspider'
    start_urls = ['https://example.com']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # Нажимаем на div
        div = response.selenium.find_element_by_xpath("//div[@class='my-class']")
        div.click()

        # Получаем содержимое скрытого блока
        hidden_block = response.selenium.find_element_by_xpath("//div[@class='hidden-block']")
        content = hidden_block.text

        yield {'content': content}