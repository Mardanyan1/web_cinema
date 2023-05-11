from concurrent.futures import ThreadPoolExecutor
import re

# #через значени находим ключ "film1"
# films = [{"film1":"link1"},{"film2":"link2"},{"film3":"link3"}]

# for film in films:
#     if "link1" in film.values():
#         key = list(film.keys())[0]
#         print(key)



# #замена пробелов на %20
# def replace_text(input_text):
#     # Удаляем пробелы в конце строки
#     trimmed_text = input_text.rstrip()

#     # Проверяем, есть ли слова после удаления пробелов
#     if trimmed_text:
#         # Заменяем пробелы между словами на %20
#         replaced_text = re.sub(r'\s+', '%20', trimmed_text)
#         return replaced_text
#     else:
#         return input_text

# # Пример использования
# text1 = "париж по"
# replaced1 = replace_text(text1)
# print(replaced1)  # Output: "париж%20по"

# text2 = "париж    "
# replaced2 = replace_text(text2)
# print(replaced2)  # Output: "париж"


with ThreadPoolExecutor(max_workers=10) as executor:#max_workers - количество потоков
    print('c')
    print('o')
    print('n')
    print('s')
    print('t')
    print('a')
    print('n')
    