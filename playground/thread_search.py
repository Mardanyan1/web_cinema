from concurrent.futures import ThreadPoolExecutor
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait

from .get_json_keys import threading_get_json_keys


def parse_site(url):
    t00 = time.time()
    options = Options()
    options.add_argument('--headless')#настройки для открытия браузера в фоне(без графики)

    driver = webdriver.Chrome(options=options)

    # Загружаем страницу
    driver.get(url)

    # Ожидаем, пока страница полностью загрузится
    # wait = WebDriverWait(driver, 5)

    # Получаем HTML-код страницы
    html = driver.page_source

    # Создаем объект BeautifulSoup из HTML-страницы
    soup = BeautifulSoup(html, 'html.parser')

    # Закрываем веб-браузер
    driver.quit()

    if 'ivi' in url:
        # Ищем нужные данные на странице ivi
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

    # # Закрываем веб-браузер
    # driver.quit()
    t11 = time.time()
    print(t11-t00)
    return film_data


def threading_search_test():
    t0 = time.time()#тест времени
    link_name="париж "
    urls = [
        'https://www.ivi.ru/search/?ivi_search='+link_name,
        # 'https://www.ivi.ru/search/?ivi_search='+'привет',        
        # 'https://www.ivi.ru/search/?ivi_search='+'он',        
        # 'https://www.ivi.ru/search/?ivi_search='+'темн',        
    ]

    with ThreadPoolExecutor(max_workers=10) as executor:# max_workers - количество потоков
        linksFilmsAllCinema = list(executor.map(parse_site, urls))# НАЧАЛО РАБОТЫ МНОГОПОТОЧНОСТИ
        print(type(linksFilmsAllCinema))
        linksFilmsAllCinema = json.dumps(linksFilmsAllCinema)
        # linksFilmsAllCinema = json.loads(linksFilmsAllCinema) #переводит текст из текста json в обычный (НО! обычный будет с одинарными кавычками, которые json не примет)
        # КОНЕЦ потока (все что под with ThreadPoolExecutor - это часть многопоточности)
    # print(linksFilmsAllCinema)
    
    #ВВЫЫЫЫОВООД
    # threading_get_json_keys(linksFilmsAllCinema)
    #вызываем парсер каждой страницы
    return threading_get_json_keys(linksFilmsAllCinema)

    t1 = time.time()
    print(t1-t0)#тест времени
# threading_search_test()#тестовый запуск


def threading_search(film_search_name):
    t0 = time.time()#тест времени
    # Удаляем пробелы в конце строки
    trimmed_text = film_search_name.rstrip()

    # Проверяем, есть ли слова после удаления пробелов
    if trimmed_text:
        # Заменяем пробелы между словами на %20
        replaced_text = re.sub(r'\s+', '%20', trimmed_text)
        link_name = replaced_text
    else:
        link_name = film_search_name
    urls = [
        'https://www.ivi.ru/search/?ivi_search='+link_name,
        # 'https://www.ivi.ru/search/?ivi_search='+'привет',        
        # 'https://www.ivi.ru/search/?ivi_search='+'он',        
        # 'https://www.ivi.ru/search/?ivi_search='+'темн',        
    ]

    with ThreadPoolExecutor(max_workers=10) as executor:# max_workers - количество потоков
        linksFilmsAllCinema = list(executor.map(parse_site, urls))# НАЧАЛО РАБОТЫ МНОГОПОТОЧНОСТИ
        print(type(linksFilmsAllCinema))
        linksFilmsAllCinema = json.dumps(linksFilmsAllCinema)
        # linksFilmsAllCinema = json.loads(linksFilmsAllCinema) #переводит текст из текста json в обычный (НО! обычный будет с одинарными кавычками, которые json не примет)
        # КОНЕЦ потока (все что под with ThreadPoolExecutor - это часть многопоточности)
    # print(linksFilmsAllCinema)
    
    #ВВЫЫЫЫОВООД
    # threading_get_json_keys(linksFilmsAllCinema)
    #вызываем парсер каждой страницы
    return threading_get_json_keys(linksFilmsAllCinema)

    t1 = time.time()
    print(t1-t0)#тест времени
