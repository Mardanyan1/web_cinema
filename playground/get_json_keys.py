from concurrent.futures import ThreadPoolExecutor
import os
import time
import uuid
import requests
from bs4 import BeautifulSoup
import json
from random import randint


def get_IVI_data_keys(json_obj):
    all_films_data = []
    for key, value in json_obj.items():
        link = key
        year = json_obj[key]['year']
        image = json_obj[key]['image']
        film_name = json_obj[key]['film_name']
        # time.sleep(randint(5,7))
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
            if script.string is not None and 'window.__INITIAL_STATE__ =' in script.string:
                json_str = script.string.split('window.__INITIAL_STATE__ =')[1].strip()
                data = json.loads(json_str)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        #удаляем файл, чтобы не было мусора
        os.remove(filename)
        #----------------------------------------------------------------------------------------------------------------


        #-----------------------------------------------Вывод json-данных фильма-----------------------------------------

        #проверка на бесплатность проекта
        element = soup.find('div', {'class': 'nbl-textBadge_style_resh'})

        film_data_json_link = data['pages']['watch']['purchaseOptions']['contentPurchaseOptions']['purchase_options']
        print("-----------------------------------------")

        #перебор всех выбранных ниже наддын по ссылке film_data_json_link
        parse_data_result = {
            'film_name': film_name,
            # 'link': link, 
            'image': image,
            'year': year
        }
        i = 0
        for item in film_data_json_link:#перебор всех возможных способов приобретения фильма
            #это условие проверяет - бесплатный ли фильм
            if element:
                isFree = True
                downloadable = "Бесплатно"
                price = "0"
                quality = "HD"
                print('Бесплатно ')
                parse_data_result[int(i)] = {
                    'cinema': 'ivi',
                    'link': link, 
                    'viewing_method':downloadable,
                    'quality':quality,
                    'price':price
                }
                i=i+1
                break

            #это условие убирает пункт по типу "подписка на фильмы WB". Можно использовать для скидок и различных условий
            if item["object_type"] == 'collection':
                continue
            #это условие убирает цену 0, так как она мне не нужна   
            if item["price"] == '0':
                continue
            
            #проверка на наличие скидок
            price = item["price"]
            findSale = item["payment_options"]
            for pr in findSale:
                salePrice = pr["user_price"]
                if salePrice == "1":
                    continue
                if int(price) == int(salePrice):
                    continue
                if int(price) < int(salePrice):
                    continue
                price = salePrice
                break
    
            object_title = item['object_title']#название фильма
            quality = item['quality'] # качество

            #пишем в тег, что это подписка
            if item["object_type"] == 'subscription':
                downloadable = 'Подписка'
                quality = 'HD'
                print(price,quality, downloadable)
                parse_data_result[int(i)] = {
                    'link': link, 
                    'cinema':'ivi',
                    'viewing_method':downloadable,
                    'quality':quality,
                    'price':price
                }
                i=i+1
                continue
            downloadable = item['downloadable']# Подписка, Покупка или Аренда
            if downloadable is True:
                downloadable='Покупка'
            else:
                downloadable = 'Аренда'

            print(price,quality, downloadable)

            parse_data_result[int(i)] = {
                'link': link, 
                'cinema':'ivi',
                'viewing_method':downloadable,
                'quality':quality,
                'price':price
            }
            i=i+1
        all_films_data.append(parse_data_result)
    return all_films_data        
        #ищешь по product_title, "downloadable": true - значит купить, "downloadable": false - значит аренда, "quality": качество
        #-------------------------------------------------------------------------------------------------------------------


def cinemas(json_obj):
    all_films_data = []
    for key in json_obj.keys():
        if 'ivi' in key:           
            # Ищем нужные данные на странице ivi
            all_films_data += get_IVI_data_keys(json_obj)
            return all_films_data
        elif 'more.tv' in key:
            # all_films_data += json_obj
            temple = []
            for keys, value in json_obj.items():
                link = keys
                # Обращение к элементам внутреннего словаря
                year = value['year']
                image = value['image']
                film_name = value['film_name']
                viewing_method = value['viewing_method']
                quality = value['quality']
                price = value['price']
                parse_data_result = {
                    'film_name': film_name,
                    'image': image,
                    'year': year,
                    0:{
                        'cinema': 'more',
                        'link': link, 
                        'viewing_method':viewing_method,
                        'quality':quality,
                        'price':price
                    }
                }            
                all_films_data.append(parse_data_result)
            return all_films_data
        else:
            
            return all_films_data

        # elif 'more' in url:



def threading_get_json_keys(linksFilmsAllCinema):
    json_list = json.loads(linksFilmsAllCinema)
    final_list = []
    #начинаем потоковый парсинг каждой страницы
    for json_obj in json_list:
        with ThreadPoolExecutor(max_workers=3) as executor:#max_workers - количество потоков
            linksFilmsAllCinema = executor.map(cinemas, [json_obj])
            linksFilmsAllCinema = list(linksFilmsAllCinema)
            if json_obj == {}:
                continue
            linksFilmsAllCinema = json.dumps(linksFilmsAllCinema)
            linksFilmsAllCinema = json.loads(linksFilmsAllCinema)
            linksFilmsAllCinema = linksFilmsAllCinema[0]
            final_list = final_list + linksFilmsAllCinema
    print("-----------------------------------------")
    new_data = []
    for item in final_list:
        film_name = item["film_name"]
        film_name = film_name.lower()
        found = False
        for new_item in new_data:
            new_film = new_item["film_name"]
            new_film = new_film.lower()
            if new_film == film_name:
                new_item[len(new_item)] = item["0"]
                found = True
                break
        if not found:
            new_data.append(item)
    print("------------------")
    print(new_data)
    return new_data
