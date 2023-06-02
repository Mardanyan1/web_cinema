from concurrent.futures import ThreadPoolExecutor
import re
import requests

# #через значени находим ключ "film1"
# films = [{"film1":"link1"},{"film2":"link2"},{"film3":"link3"}]

# for film in films:
#     if "link1" in film.values():
#         key = list(film.keys())[0]
#         print(key)



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from fake_useragent import UserAgent

def parse_search():
    options = Options()
    options.add_argument('--headless')
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })
    options.add_argument(f'user-agent={s.headers["User-Agent"]}')
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://yandex.ru/search/?text=парижская+1900+okko')


    time.sleep(2)  # Даем время для загрузки страницы

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    first_link = soup.find('a', class_='serp-item__title-link')
    # first_link = first_link.get("href")
    links = []
    for elem in first_link:
        links.append(elem.get("href"))
        print("First link:", first_link)

    print("First link:", first_link)

    driver.quit()

    if 'Okko.tv' in first_link:
        # Условие A
        print("Условие A")
    else:
        # Условие B
        print("Условие B")

parse_search()
