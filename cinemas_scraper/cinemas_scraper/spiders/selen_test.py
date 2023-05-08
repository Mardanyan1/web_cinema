from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import TextResponse


import scrapy, time


class IvSpider(scrapy.Spider):
    name = 'sel_test'
    start_urls = ['https://www.ivi.ru/movies/all']
    
    def parse(self, response):
        for link in response.css('ul.gallery__list li.gallery__item a::attr(href)'):
            # driver.get(link)
            # button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".nbl-button_style_ran nbl-button_size_shinnok")))
            # button.click()
            # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.result-class")))
            # result = element.text
            driver = webdriver.Chrome()
            driver.get(link)
            button = driver.find_element(By.CSS_SELECTOR, ".nbl-button_style_ran nbl-button_size_shinnok")
            button.click()
            time.sleep(5) # Ждем 5 секунд, чтобы страница успела загрузиться
            body = driver.page_source
            response = TextResponse(url=driver.current_url, body=body, encoding='utf-8')
            driver.quit()
            yield scrapy.Request(url=response.url, callback=self.parse, body=response.body)
            # yield response.follow(link, callback=self.parse_films)

        for i in range(1,3):
            next_page = f'https://www.ivi.ru/movies/all/page{i}'
            
            yield response.follow(next_page, callback=self.parse)
        # i=1
        # while(next_page is not None):
        #     i=i+1
        #     next_page = f'https://www.ivi.ru/movies/all/page{i}'
        #     yield response.follow(next_page, callback=self.parse)
        
    def parse_films(self, response):
        yield{
            'film':response.css('div.watchTitle__title::text').get(),
            'languages':response.css('div.watchOptions__values::text').get()
        }
