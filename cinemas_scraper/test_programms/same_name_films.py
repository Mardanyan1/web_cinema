import json
import os
import uuid
from bs4 import BeautifulSoup
import requests

link = "https://wink.ru/movies/parizh-tekhas-year-1984"
response = requests.get(link)

#-----------------------------------------------Поиск json-файла------------------------------------------------
#создаем файл example, куда будем записывать весь html файл
filename = str(uuid.uuid4()) + ".html"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(response.text)
#передаем html файл в переменную в виде текста
with open(filename, 'r', encoding='utf-8') as f:
    html_parsing = f.read()
#не углублялся, но этот кусок находит нужную мне часть кода и и сохраняет его отдельны json файлом
soup = BeautifulSoup(html_parsing, 'html.parser')
scripts = soup.find_all('script')
for script in scripts:
    if script.string is not None and 'window.__REACT_QUERY_STATE__=' in script.string:
        json_str = script.string.split('window.__REACT_QUERY_STATE__=')[1].strip()
        data = json.dumps(json_str)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
#удаляем файл, чтобы не было мусора
os.remove(filename)