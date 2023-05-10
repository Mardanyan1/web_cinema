from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

# [
#     {'Париж подождет': 'https://www.ivi.ru/watch/155935', 'Париж, вино и романтика': 'https://www.i',
#      'Париж: Город мёртвых': 'https://www.ivi.ru/watch/121559', 'Трамвай в Париж': 'https://www.ivtch/2750'
#      }, 
#     {'Блэк': 'https://www.ivi.ru/watch/blek', 'Темный мир: Равновесие': 'https://www.iviзеркало': 'https://www.ivi.ru/watch/224254', 
#      'Темные воды': 'https://www.ivi.ru/watch/348930', '//www.ivi.ru/watch/137606', 'Темное наследие': 'https://www.ivi.ru/watch/424055', 
#      'Темные тайны': 'https://www.ivi.ru/watch/102427', 'Темные дороги': 'https://www.ivi.ru/watch/205375', 
#      '[4k] Трансформеры 3: Тёмная сtps://www.ivi.ru/watch/172253', 'Врата Аграмона': 'https://www.ivi.ru/watch/462884', 
#      'Девятые врs://www.ivi.ru/watch/452776', 'Лев Яшин. Вратарь моей мечты': 'https://www.ivi.ru/watch/185741'
#      }
# ]

# попробуй через цикл пропарсить каждый фильм. Парсинг по сути готов, тебе просто нужно вместо url поставить нужные значения, 
# а потом в виде json вложить в старый список по типу:
# "film_num_#1": [{
#                     "film_name": 'Париж подождет',
#                     "film_link": 'https://www.ivi.ru/watch/155935',
#                     "prices": {
#                         "min": "129",
#                         "max": "599"
#                     }
#                   }]
# from cinemas_scraper.selenium_drivers.thread_search import parse_site

# a = parse_site()


t0 = time.time()
ua = UserAgent()
headers = {'accept': '*/*', 'user-agent': ua.chrome}

# получаем html-страницу сайта
url = 'https://www.ivi.ru/search/?ivi_search=париж%20по'

# response = requests.get(url, headers=headers)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Загружаем страницу
driver.get(url)

# Ожидаем, пока страница полностью загрузится
wait = WebDriverWait(driver, 5)

# Получаем HTML-код страницы
html = driver.page_source

# Создаем объект BeautifulSoup из HTML-страницы
soup = BeautifulSoup(html, 'html.parser')




#надо засунуть data и links в словарь 




# Ищем нужные данные на странице
film_name_elem = soup.find_all('span', class_='nbl-slimPosterBlock__titleText')
links_elems = soup.find_all('a', class_='nbl-slimPosterBlock_available')

links = []
for elem in links_elems:
    links.append(elem.get("href"))


# Выводим данные в консоль
film_name = []
for item in film_name_elem:
    film_name.append(item.text)

pairs = zip(film_name, links)

# Генерируем словарь из списка кортежей
film_data = {k: v for k, v in pairs}

# Печатаем итоговый словарь
print(film_data)

# Закрываем веб-браузер
driver.quit()
t1 = time.time()
print(t1-t0)