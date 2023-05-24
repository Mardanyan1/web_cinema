import requests
import json

base_url = "https://api2.ivi.ru/mobileapi/catalogue/v7/"
category_id = 14
from_value = 1
to_value = 50
app_version = 870
film_count=0

result_list = []


while True:
    url = f"{base_url}?category={category_id}&from={from_value}&to={to_value}&withpreorderable=true&app_version={app_version}"
    response = requests.get(url)
    data = response.json()
    
    results = data.get('result', [])
    for result in results:
        year = result.get('year')
        title = result.get('title')
        link = result.get('share_link')
        #получение изображения
        posters = result.get('posters', [])
        img = posters[0]['url'] if posters else None

        # Обработка и использование значения year
        # print(f"Year: {year}")
        film_count=film_count+1

        # Добавление значения year в список результатов
        result_list.append({"title":title, "year": year, "link":link, "image":img})
    
    # Увеличение значений from_value и to_value для следующего запроса
    from_value += 50
    to_value += 50
    
    # Выход из цикла, если больше нет результатов
    if not results:
        break
print(result_list)

# Сохранение результатов в JSON-файл
with open("results_ivi.json", 'w', encoding='utf-8') as file:
    json.dump(result_list, file, ensure_ascii=False, indent=4)