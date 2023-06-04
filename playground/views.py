import time
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .thread_search import threading_search
from .forms import FilmsCostForm, InputForm, Like_filmsForm
from .models import TEST_Like_films, Films, Like_films, Films_Cost
from django.contrib.auth.decorators import user_passes_test




def test_text(request):
    like_films = TEST_Like_films.objects.all()
    return render(request, 'playground/exmple.html',  {'title':'ТЕСТОВАЯ', 'like_films':like_films})

def say_hello(request):
    return render(request, 'playground/hello.html', {'name':'Artyom','title':'Hello User'})


def main_page(request):
    like_films = TEST_Like_films.objects.all()
    return render(request, 'playground/main_page.html', {'title':'Главная страница', 'like_films':like_films})


def wir(request, id_filmRequest):
    cost_films = get_object_or_404(Films_Cost, id_filmRequest=id_filmRequest)
    error = ''
    if request.method == 'POST':
        film_name = request.POST.get('film_name')
        print("---------------")
        print(film_name)

        year = request.POST.get('year')
        print("---------------")
        print(year)

        cost_films = Films_Cost.objects.get(parameter1=film_name, parameter2=year)
        print("---------------")
        print(cost_films)

        cost_films = cost_films.id_film()
        print("---------------")
        print(cost_films)
        
        form = FilmsCostForm(request.POST, instance=cost_films)
        if form.is_valid():
            form.save()
            return redirect('greetings')
        else:
            error = 'form was wrong'
    else:
        form = FilmsCostForm(instance=cost_films)
    context = {
        'form':form,
        'title':'Сохранить?'
    }
    return render(request, 'playground/about_us.html', context)

#поле создания новых данных, которое доступен только авторизированным пользователям с ролью superuser(admin)
@user_passes_test(lambda u: u.is_superuser)
@login_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = Like_filmsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('greetings')
        else:
            error = 'form was wrong'

    form = Like_filmsForm()
    context = {
        'form':form,
        'title':'create'
    }
    return render(request, 'playground/create.html', context)

#поле удаления данных, которое доступен только авторизированным пользователям с ролью superuser(admin)
@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete(request, id):
    obj = get_object_or_404(TEST_Like_films, id=id)
    if request.method == "POST" and request.POST.get("delete"):
        obj.delete()
        return redirect('greetings')
    context = {
        'object': obj,
        'title':'Delete'
    }
    return render(request, "playground/delete.html", context)


#поле обновления данных, которое доступен только авторизированным пользователям с ролью superuser(admin)
@user_passes_test(lambda u: u.is_superuser)
@login_required
def update(request, id):
    like_films = get_object_or_404(TEST_Like_films, id=id)
    error = ''
    if request.method == 'POST':
        form = Like_filmsForm(request.POST, instance=like_films)
        if form.is_valid():
            form.save()
            return redirect('greetings')
        else:
            error = 'form was wrong'
    form = Like_filmsForm(instance=like_films)
    context = {
        'form':form,
        'title':'Update'
    }
    return render(request, 'playground/update.html', context)





def search_movie(request):
    if request.method == 'GET':
        t1 = time.time()
        film_search_name = request.GET.get('film_search_name')  # Получаем текст из поля ввода с именем 'film_search_name'
        
        # Передаем полученное название фильма в функцию для парсинга
        movie_list = threading_search(film_search_name)
        t0 = time.time()
        print(t0-t1)#тест времени
        for movie_data in movie_list:
            film_name = movie_data['film_name']
            print("---------------")
            print(film_name)

            year = movie_data['year']
            print("---------------")
            print(year)

            photo = movie_data['image']
            # Проверка, существует ли уже фильм с похожими параметрами
            existing_movie = Films.objects.filter(film_name=film_name, year=year) #.first()

            if not existing_movie:
                # Фильм еще не существует, сохраняем его
                # Создание экземпляра модели Films
                movie = Films(film_name=film_name, year=year, photo=photo)
                movie.save()
                print("СОХРАНИЛ")

            for key, value in movie_data.items() :#перебор всех возможных способов приобретения фильма
            #это условие проверяет - бесплатный ли фильм
                if isinstance(value, dict):
                    link = value['link']
                    viewing_method = value['viewing_method']
                    quality = value['quality']
                    price = value['price']
                
                    film = Films.objects.get(film_name=film_name)
                    film_id = film.id_film

                    existing_movie_cost = Films_Cost.objects.filter(viewing_method=viewing_method,quality=quality,link=link) #.first()
                    if existing_movie_cost:
                        # Фильм уже существует, пропускаем его сохранение
                        continue
                    film_cost = Films_Cost(viewing_method=viewing_method,quality=quality,cost=price,link=link,id_film=film)
                    film_cost.save()

        # Возвращаем пользователю страницу с результатами
        return render(request, 'playground/movie_results.html', {'title':'Результаты поиска','movie_data': movie_list})
    
    if request.method == 'POST':
        
        film_name = request.POST.get('film_name')

        link = request.POST.get('link')

        year = request.POST.get('year')

        price = request.POST.get('price')

        viewing_method = request.POST.get('viewing_method')

        quality = request.POST.get('quality')

        # Находим объект Films_Cost по ссылке
        film_cost = Films_Cost.objects.filter(link=link).first()
        film_cost_id = film_cost.id_film
        # Получаем текущего зарегистрированного пользователя
        current_user = request.user

        # Находим все записи в Films_Cost с таким же id_film, как у найденного film_cost
        related_films = Films_Cost.objects.filter(id_film=film_cost_id)
        print("-----------")
        print(related_films)
        print("-----------")
        # Сохраняем все связанные фильмы в таблице Like_films с указанием текущего пользователя
        for film in related_films:
            existing_movie = Like_films.objects.filter(id_filmRequest=film, user=current_user)#.first()
            if existing_movie:
                # Фильм уже существует, пропускаем его сохранение
                print("ТАКОЙ ЕЕЕЕЕЕСТЬ")
                break
            like_film = Like_films(id_filmRequest=film, user=current_user)
            like_film.save()



        # film_name = request.POST.get('film_name')
        # print("---------------")
        # print(film_name)

        # link = request.POST.get('link')
        # print("---------------")
        # print(link)

        # year = request.POST.get('year')
        # print("---------------")
        # print(year)

        # price = request.POST.get('price')
        # print("---------------")
        # print(str(price))

        # viewing_method = request.POST.get('viewing_method')
        # print("---------------")
        # print(viewing_method)

        # quality = request.POST.get('quality')
        # print("---------------")
        # print(quality)

        # film = Films.objects.get(film_name=film_name)
        # print("---------------")
        # print(film)
        # film_id = film.id_film
        # print("---------------")
        # print(film_id)

        # existing_movie = Films_Cost.objects.filter(viewing_method=viewing_method,quality=quality,link=link)#.first()
        # if existing_movie:
        #     # Фильм уже существует, пропускаем его сохранение
        #     print("ТАКОЙ ЕЕЕЕЕЕСТЬ")
        # film_cost = Films_Cost(viewing_method=viewing_method,quality=quality,cost=price,link=link,id_film=film)
        # film_cost.save()







        # cost_films = cost_films.id_film()
        # print("---------------")
        # print(cost_films)
        

        # form = FilmsCostForm(request.POST, instance=film_cost)
        # if form.is_valid():
        #     form.save()
        #     return redirect('playground/main_page.html')  # Редирект на страницу успешного сохранения
    else:
        print("сразу пропуск")
        print(form.errors)
        form = FilmsCostForm()
    # return render(request, 'playground/hello.html')

    # Если запрос не является GET-запросом, отображаем пустую форму
    return render(request, 'registration/profile.html')