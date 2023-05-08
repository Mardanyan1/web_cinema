import requests
from bs4 import BeautifulSoup
import json

# Making a get request

response = requests.get('https://www.ivi.ru/watch/98531')

# response = requests.get('https://www.ivi.ru/watch/145156')

#создаем файл example, куда будем записывать весь html файл
with open('example.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

#передаем html файл в переменную в виде текста
with open('example.html', 'r', encoding='utf-8') as f:
    html_parsing = f.read()

#не углублялся, но этот кусок находит нужную мне часть кода и и сохраняет его отдельны json файлом
soup = BeautifulSoup(html_parsing, 'html.parser')
scripts = soup.find_all('script')
for script in scripts:
    if script.string is not None and 'window.__INITIAL_STATE__ =' in script.string:
        json_str = script.string.split('window.__INITIAL_STATE__ =')[1].strip()
        script_parsing = json.loads(json_str)
        with open('script_parsing.json', 'w', encoding='utf-8') as f:
            json.dump(script_parsing, f)

#проверяю для себя сохранилось ли
with open('script_parsing.json', 'r', encoding='utf-8') as f:
    #print(f.read())
    data = json.load(f)

json_link = data['pages']['watchPage']['purchaseOptions']['contentPurchaseOptions']['purchase_options']

for item in json_link:
    price = item['price']
    object_title = item['object_title']#название фильма
    product_title = item['product_title']
    quality = item['quality']
    downloadable = item['downloadable']
    if downloadable is True:
        downloadable='Поукпка'
    else:
        downloadable = 'Аренда'
    print(price, product_title,quality, downloadable)
print(object_title)

#ищешь по product_title, "downloadable": true - значит купить, "downloadable": false - значит аренда, "quality": качество