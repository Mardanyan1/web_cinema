from concurrent.futures import ThreadPoolExecutor
import os
import uuid
import requests
from bs4 import BeautifulSoup
import json


# [
#     {'Париж подождет': 'https://www.ivi.ru/watch/155935', 'Париж, вино и романтика': 'https://www.i',
#      'Париж: Город мёртвых': 'https://www.ivi.ru/watch/121559', 'Трамвай в Париж': 'https://www.ivtch/2750'
#      }, 
#     {'Блэк': 'https://www.ivi.ru/watch/blek', 'Темный мир: Равновесие': 'https://www.iviзеркало': 'https://www.ivi.ru/watch/224254', 
#      'Темные воды': 'https://www.ivi.ru/watch/348930', '//www.ivi.ru/watch/137606', 'Темное наследие': 'https://www.ivi.ru/watch/424055', 
#      'Темные тайны': 'https://www.ivi.ru/watch/102427', 'Темные дороги': 'https://www.ivi.ru/watch/205375', 
#      '[4k] Трансформеры 3: Тёмная сtps://www.ivi.ru/watch/172253', 'Врата Аграмона': 'https://www.ivi.ru/watch/462884', 
#      'Лев Яшин. Вратарь моей мечты': 'https://www.ivi.ru/watch/185741'
#      }
# ]

# попробуй через цикл пропарсить каждый фильм. Парсинг по сути готов, тебе просто нужно вместо url поставить нужные значения, 
# а потом в виде json вложить в старый список по типу:
# "film_num_#1": [{
#                     "film_name": 'Париж подождет',
#                     "film_link": 'https://www.ivi.ru/watch/155935',
#                     "prices": [
#                         "min": "129",
#                         "max": "599"
#                     ]
#                   }]



def get_data_keys(json_obj):
    all_films_data = []
    for key, value in json_obj.items():
        film_name = key
        link = value
        #------------------------------------------ТЕСТОВЫЕ ССЫЛКИ------------------------------------------------------

        # response = requests.get('https://www.ivi.ru/watch/98531') #Анаболики - покупка (мб подписка)

        # response = requests.get('https://www.ivi.ru/watch/horoshij-doktor')# Хороший доктор - подписка (почему то пишет данные сериала "Хороший доктор")

        # response = requests.get('https://www.ivi.ru/watch/109726') # 1+1 - подписка (почему то пишет данные сериала "Хороший доктор") 
                                                                    #!!!!!! короче, просто берем название из парсера поисковика сайта - так легче будет

        # response = requests.get('https://www.ivi.ru/watch/216926') #Джентельмены - покупка

        # response = requests.get('https://www.ivi.ru/watch/486832')

        response = requests.get(link)
        #---------------------------------------------------------------------------------------------------------------


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
        #удаляем файл, чтобы не было мусора
        os.remove(filename)
        #----------------------------------------------------------------------------------------------------------------


        #-----------------------------------------------Вывод json-данных фильма-----------------------------------------

        #проверка на бесплатность проекта
        element = soup.find('div', {'class': 'nbl-textBadge_style_resh'})



        film_data_json_link = data['pages']['watchPage']['purchaseOptions']['contentPurchaseOptions']['purchase_options']
        print("-----------------------------------------")

        #перебор всех выбранных ниже наддын по ссылке film_data_json_link
        parse_data_result = {
            'film_name': film_name,
            'link': link
        }
        i = 0
        for item in film_data_json_link:
            #это условие проверяет - бесплатный ли фильм
            if element:
                isFree = True
                downloadable = "Бесплатно"
                price = "0"
                quality = "HD"
                print('Бесплатно ')
                parse_data_result[str(i)] = {
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

            price = item['price']
            object_title = item['object_title']#название фильма
            quality = item['quality'] # качество

            #пишем в тег, что это подписка
            if item["object_type"] == 'subscription':
                downloadable = 'Подписка'
                quality = 'HD'
                print(price,quality, downloadable)
                parse_data_result[str(i)] = {
                    'viewing_method':downloadable,
                    'quality':quality,
                    'price':price
                }
                i=i+1
                continue

            downloadable = item['downloadable']# Подписка, Покупка или Аренда
            if downloadable is True:
                downloadable='Поукпка'
            else:
                downloadable = 'Аренда'

            print(price,quality, downloadable)

            parse_data_result[str(i)] = {
                'viewing_method':downloadable,
                'quality':quality,
                'price':price
            }
            i=i+1
        all_films_data.append(parse_data_result)
    return all_films_data
    print("-------------------------------------SIIIIIIIIIIIII-----------------")
    print(parse_data_result)
        
        # print("-----------------------------------------")
        
        #ищешь по product_title, "downloadable": true - значит купить, "downloadable": false - значит аренда, "quality": качество
        #-------------------------------------------------------------------------------------------------------------------


def threading_get_json_keys(linksFilmsAllCinema):
    json_list = json.loads(linksFilmsAllCinema)
    #начинаем потоковый парсинг каждой страницы
    for json_obj in json_list:
        with ThreadPoolExecutor(max_workers=10) as executor:#max_workers - количество потоков
            linksFilmsAllCinema = executor.map(get_data_keys, [json_obj])
            linksFilmsAllCinema = list(linksFilmsAllCinema)
            linksFilmsAllCinema = json.dumps(linksFilmsAllCinema)
            linksFilmsAllCinema = json.loads(linksFilmsAllCinema)
            linksFilmsAllCinema = linksFilmsAllCinema[0]
            print(type(linksFilmsAllCinema))
    print(linksFilmsAllCinema)
    return linksFilmsAllCinema
