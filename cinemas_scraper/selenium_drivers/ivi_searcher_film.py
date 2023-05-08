from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

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

# links = soup.find_all('a', class_='nbl-slimPosterBlock_available').get("href")

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