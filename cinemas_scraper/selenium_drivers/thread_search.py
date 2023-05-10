from concurrent.futures import ThreadPoolExecutor
import json
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
    film_name_elem = soup.find_all('span', class_='nbl-slimPosterBlock__titleText')
    links_elems = soup.find_all('a', class_='nbl-slimPosterBlock_available')
    #через цикл сохраняем в массив
    links = []
    for elem in links_elems:
        links.append(elem.get("href"))

    #через цикл сохраняем в массив
    film_name = []
    for item in film_name_elem:
        film_name.append(item.text)

    #объединяем в словарь
    pairs = zip(film_name, links)

    # Генерируем словарь из списка кортежей
    film_data = {k: v for k, v in pairs}

    # Закрываем веб-браузер
    driver.quit()
    return film_data

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
        # print(results)#обычнаяя проверка инфы
        print(type(results))
        results = json.dumps(results)
        # results = json.loads(results) #переводит текст из текста json в обычный (НО! обычный будет с одинарными кавычками, которые json не примет)
        print(results)
        t1 = time.time()
        print(t1-t0)#тест времени