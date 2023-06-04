from concurrent.futures import ThreadPoolExecutor
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent

from get_json_keys import threading_get_json_keys


def parse_site(url):
    t00 = time.time()
    
    options = Options()
    options.add_argument('--headless')#настройки для открытия браузера в фоне(без графики)
    # ua = UserAgent()
    # user_agent = ua.random
    # options.add_argument(f'--user-agent={user_agent}')
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

    options.add_argument(f'user-agent={s.headers["User-Agent"]}')
    driver = webdriver.Chrome(options=options)

    # Загружаем страницу
    driver.get(url)

    # Ожидаем, пока страница полностью загрузится
    # wait = WebDriverWait(driver, 5)

    # Получаем HTML-код страницы
    html = driver.page_source

    # Создаем объект BeautifulSoup из HTML-страницы
    soup = BeautifulSoup(html, 'html.parser')

    if 'ivi' in url:
        images, years, links, film_name, viewing_methods, prices, qualitys = ivi_base_info(soup)
    elif 'okko' in url:
        film_name_elem = soup.find_all('span', class_='RQ6wn_Q0')
        links_elems = soup.find_all('a', class_='vj8iwpkR')  
    elif 'more' in url:
        images, years, links, film_name, viewing_methods, prices, qualitys = more_base_info(soup)
    elif 'wink.ru' in url:
        film_name_elem = soup.find_all('span', class_='RQ6wn_Q0')
        links_elems = soup.find_all('a', class_='vj8iwpkR')  

    # Генерируем словарь из списка кортежей
    film_data1 = {}
    for i, (link, (image, year, name,viewing_method,price,quality)) in enumerate(zip(links, zip(images, years, film_name,viewing_methods,prices,qualitys)), start=1):
        film_data1[link] = {
            'image': image,
            'year': year,
            'film_name': name,
            'viewing_method':viewing_method,
            'price':price,
            'quality':quality
        }
    # Закрываем веб-браузер
    driver.quit()
    t11 = time.time()
    print(t11-t00)
    return film_data1



def ivi_base_info(soup):
    # Ищем нужные данные на странице ivi
    film_name_elem = soup.find_all('span', class_='nbl-slimPosterBlock__titleText')
    links_elems = soup.find_all('a', class_='nbl-slimPosterBlock_available')
    image_elems = soup.find_all('img', alt=True, class_='nbl-poster__image')
    properties = soup.find_all('div', class_='nbl-poster__properties')
    #через цикл сохраняем в массив
    images = []
    for item in image_elems:
        images.append(item.get("src"))

    #через цикл сохраняем в массив
    years = []
    for prop in properties:
        properties_info = prop.find('div', class_='nbl-poster__propertiesInfo')
        properties_row = properties_info.find('div', class_='nbl-poster__propertiesRow')
        year = properties_row.text.strip().split(',')[0]  # Получение года и удаление лишних пробелов
        years.append(year)

    #через цикл сохраняем в массив
    links = []
    for elem in links_elems:
        links.append(elem.get("href"))

    #через цикл сохраняем в массив
    film_name = []
    viewing_methods = []
    prices = []
    quality = []
    for item in film_name_elem:
        film_name.append(item.text)
        viewing_methods.append('none')
        prices.append('none')
        quality.append('none')

    return images, years, links, film_name, viewing_methods, prices, quality


def more_base_info(soup):
    pre_content = soup.pre.string
    more_json_data = json.loads(pre_content)
    links = []
    film_name = []
    years = []    
    images = []
    viewing_methods = []
    prices = []
    quality = []
    for i in range(len(more_json_data['projects'])):
        film_title = more_json_data['projects'][i]['title']
        print(film_title)
        film_name.append(film_title)
        link = more_json_data['projects'][i]['canonicalUrl']
        links.append('https://more.tv' + link)
        year = more_json_data['projects'][i]['releaseDate'][:4]
        years.append(year)
        image = more_json_data['projects'][i]['projectPosterGallery']['JPEG']['W250H355']['url']
        images.append(image)
        viewing_method = more_json_data['projects'][i]['subscriptionType']
        if viewing_method == 'FREE':
            viewing_method = 'Бесплатно'
            price = '0'
        else:
            viewing_method = 'Подписка'
            price = '299'
        viewing_methods.append(viewing_method)
        prices.append(price)
        quality.append("HD")

    return images, years, links, film_name, viewing_methods, prices, quality








def threading_search_test():
    link_name="париж я люблю тебя "
    urls = [
        'https://www.ivi.ru/search/?ivi_search='+link_name,
        # 'https://okko.tv/search/'+link_name,        
        'https://more.tv/upuaut/v4/web/suggest?q='+link_name,        
        # 'https://wink.ru/search?query='+link_name,        
    ]

    with ThreadPoolExecutor(max_workers=10) as executor:# max_workers - количество потоков
        linksFilmsAllCinema = list(executor.map(parse_site, urls))# НАЧАЛО РАБОТЫ МНОГОПОТОЧНОСТИ
        print(type(linksFilmsAllCinema))
        linksFilmsAllCinema = json.dumps(linksFilmsAllCinema)
    #вызываем парсер каждой страницы
    return threading_get_json_keys(linksFilmsAllCinema)

threading_search_test()#тестовый запуск






def threading_search(film_search_name):
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
        # 'https://okko.tv/search/'+link_name,        
        'https://more.tv/upuaut/v4/web/suggest?q='+link_name,        
        # 'https://www.ivi.ru/search/?ivi_search='+'темн',        
    ]
    with ThreadPoolExecutor(max_workers=10) as executor:# max_workers - количество потоков
        linksFilmsAllCinema = list(executor.map(parse_site, urls))# НАЧАЛО РАБОТЫ МНОГОПОТОЧНОСТИ
        print(type(linksFilmsAllCinema))
        linksFilmsAllCinema = json.dumps(linksFilmsAllCinema)
    #вызываем парсер каждой страницы
    return threading_get_json_keys(linksFilmsAllCinema)
        # linksFilmsAllCinema = json.loads(linksFilmsAllCinema) #переводит текст из текста json в обычный (НО! обычный будет с одинарными кавычками, которые json не примет)