
#через значени находим ключ "film1"
films = [{"film1":"link1"},{"film2":"link2"},{"film3":"link3"}]

for film in films:
    if "link1" in film.values():
        key = list(film.keys())[0]
        print(key)