# Web Cinema Project

## Описание

Web Cinema — это веб-приложение для агрегации предложений из онлайн-кинотеатров, разработанное с использованием Python (Django и BeautifulSoup4) и баз данных SQL (MySQL). Приложение позволяет пользователям искать фильмы и сериалы, получать информацию о доступности контента по подписке или покупке, а также выбирать подходящий способ просмотра.

## Функциональность

- **Агрегация данных**: Сбор информации из различных онлайн-кинотеатров по запросам пользователей с помощью веб-скрапинга, реализованного через `BeautifulSoup`.

- **Регистрация и авторизация**: Возможность зарегистрироваться и авторизироваться для удобного хранения фильмов

- **Интерфейс пользователя**: Удобный веб-интерфейс для поиска и просмотра предложений с использованием Django templates.

- **Хранение данных**: Функции добавления и удаления данных для сохранения и сравнения информации о фильмах и сериалах.

## Основные функции

- **`parse_site(url)`**: Отвечает за скрапинг данных с указанного URL-адреса. Создает объект браузера с помощью Selenium, загружает страницу, получает HTML-код и создает объект BeautifulSoup для парсинга. Ищет данные о фильмах (названия и ссылки) и сохраняет их в словари в формате "название фильма: ссылка". Возвращает полученный словарь и закрывает браузер.
- **`threading_search(film_search_name)`**: Выполняет многопоточный поиск фильмов на нескольких веб-сайтах. Принимает строку с названием фильма, формирует список URL-адресов для поиска и запускает функцию parse_site в многопоточном режиме с использованием ThreadPoolExecutor. Сохраняет результаты парсинга в список, который преобразуется в JSON и передается в threading_get_json_keys для дальнейшей обработки.
- **`threading_get_json_keys(linksFilmsAllCinema)`**: Принимает список словарей с названиями фильмов и ссылками, проходит по каждому ключу и значению, вызывая многопоточно функцию get_data_keys, собирая информацию о каждом фильме.
- **`get_data_keys(json_obj)`**: Принимает объект JSON и проходит по каждому ключу и значению, собирая информацию о каждом фильме.



## Стек технологий

- **Backend**: Python, Django, BeautifulSoup4
- **Database**: MySQL
- **Frontend**: HTML, CSS, Jinja



## Структура проекта

- **playground/**: Основные модули приложения, включая модели, представления и парсеры.
- **templates/**: HTML-шаблоны для отображения данных.
- **registration/**: Модули приложения отвечающие за регистрацию пользователя

