from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait


def parse_site(url):
    
    options = Options()
    options.add_argument('--headless')#настройки для открытия браузера в фоне(без графики)

    driver = webdriver.Chrome(options=options)

    # Загружаем страницу
    driver.get(url)

    # Ожидаем, пока страница полностью загрузится
    wait = WebDriverWait(driver, 5)

    # Получаем HTML-код страницы
    html = driver.page_source

    # Создаем объект BeautifulSoup из HTML-страницы
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем нужные данные на странице
    data = soup.find_all('span', class_='nbl-slimPosterBlock__titleText')

    # Выводим данные в консоль
    result =[]
    for item in data:
        # print(item.text)
        result += [item.text]
    
    # Закрываем веб-браузер
    driver.quit()
    return result

if __name__ == '__main__':
    t0 = time.time()#тест времени
    urls = [
        'https://www.ivi.ru/search/?ivi_search=париж%20по', 
        'https://www.ivi.ru/search/?ivi_search=темный', 
        'https://www.ivi.ru/search/?ivi_search=врата'
        ]
    results_dict = {}

    with ThreadPoolExecutor(max_workers=10) as executor:#max_workers - количество потоков
        results = executor.map(parse_site, urls)#начало многопоточной обработки поисковых запросов
        results = list(executor.map(parse_site, urls))#объединение результатов поисковых запросов
        print(results)#обычнаяя проверка инфы

        t1 = time.time()
        print(t1-t0)#тест времени