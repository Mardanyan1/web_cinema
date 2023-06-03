import json


data = [
    {
        "film_name": "\u0412\u0435\u0447\u0435\u0440\u0438\u043d\u043a\u0430 \u043f\u043e \u0441\u043b\u0443\u0447\u0430\u044e \u0440\u0430\u0437\u0432\u043e\u0434\u0430",
        "image": "https://thumbs.dfs.ivi.ru/storage30/contents/0/9/ae7ead3427321f3f64c1e9802c921c.jpg/234x360/?q=85",
        "year": "2019",
        "0": {
            "cinema": "ivi",
            "link": "https://www.ivi.ru/watch/470622",
            "viewing_method": "\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e",
            "quality": "HD",
            "price": "0"
        }
    },
    {
        "film_name": "\u0412\u0435\u0447\u0435\u0440\u0438\u043d\u043a\u0430 \u043f\u043e \u0441\u043b\u0443\u0447\u0430\u044e \u0440\u0430\u0437\u0432\u043e\u0434\u0430",
        "image": "https://static.more.tv/jackal/3911269/55b98a8e-8221-43aa-9604-e59f006586dd_W250_H355.jpg",
        "year": "2017",
        "0": {
            "link": "https://more.tv/vecherinka_po_sluchayu_razvoda",
            "cinema": "more",
            "viewing_method": "\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e",
            "quality": "HD",
            "price": "0"
        }
    },
    {
        "film_name": "\u0412\u0435\u0447\u0435\u0440\u0438\u043d\u043a\u0430 \u043f\u043e \u0441\u043b\u0443\u0447\u0430\u044e \u0440\u0430\u0437\u0432\u043e\u0434\u0430",
        "image": "https://static.more.tv/jackal/3911269/55b98a8e-8221-43aa-9604-e59f006586dd_W250_H355.jpg",
        "year": "2017",
        "0": {
            "link": "https://more.tv/vecherinka_po_sluchayu_razvoda",
            "cinema": "more",
            "viewing_method": "\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e",
            "quality": "HD",
            "price": "0"
        }
    },
    {
        "film_name": "\u041c\u043e\u043d\u0441\u0442\u0440 \u0432 \u041f\u0430\u0440\u0438\u0436\u0435",
        "image": "https://thumbs.dfs.ivi.ru/storage6/contents/a/0/c36f9c509b27ed7ee1295432a224a8.jpg/234x360/?q=85",
        "year": "2010",
        "0": {
            "link": "https://www.ivi.ru/watch/60800",
            "cinema": "ivi",
            "viewing_method": "\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e",
            "quality": "HD",
            "price": "0"
        }
}
]

new_data = []
for item in data:
    film_name = item["film_name"]
    found = False
    for new_item in new_data:
        if new_item["film_name"] == film_name:
            new_item[len(new_item)] = item["0"]
            found = True
            break
    if not found:
        new_data.append(item)

print(new_data)

print("------------------")
new_data = json.dumps(new_data)
print(new_data)