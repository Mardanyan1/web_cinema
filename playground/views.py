from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .thread_search import threading_search
from .forms import InputForm, Like_filmsForm
from .models import TEST_Like_films, Films
from django.contrib.auth.decorators import user_passes_test




def test_text(request):
    like_films = TEST_Like_films.objects.all()
    return render(request, 'playground/exmple.html',  {'title':'ТЕСТОВАЯ', 'like_films':like_films})

def say_hello(request):
    return render(request, 'playground/hello.html', {'name':'Artyom','title':'Hello User'})


def main_page(request):
    like_films = TEST_Like_films.objects.all()
    return render(request, 'playground/main_page.html', {'title':'Главная страница', 'like_films':like_films})


def wir(request):
    return render(request, 'playground/about_us.html', {'title':'О нас'})

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




# def process_input(request):
#     if request.method == 'POST':
#         form = InputForm(request.POST)
#         if form.is_valid():
#             input_text = form.cleaned_data['my_input']
#             i=0
#             while i<10:
#                 i = i+1
#                 print(input_text)
#             # Выполняйте необходимые операции с полученным значением input_text
#             # Например, сохраните его в базу данных или обработайте как требуется
            
#             return render(request, 'result.html', {'input_text': input_text})
#     else:
#         form = InputForm()
    
#     return render(request, 'myform.html', {'form': form})


def search_movie(request):
    if request.method == 'GET':
        film_search_name = request.GET.get('film_search_name')  # Получаем текст из поля ввода с именем 'film_search_name'
        # parse_data_result = {
        #     'film_name': film_search_name,
        #     'link': 'https://link',#тест
        #     '1':{
        #         'viewing_method':'Покупка',
        #         'quality':'HD',
        #         'price':'129'
        #         }
        # }
        # Передаем полученное название фильма в функцию для парсинга
        movie_data = threading_search(film_search_name)
        
        # # Создаем новую запись в базе данных с полученными данными
        # movie = Films(
        #     film_name = movie_data[''],
        #     title=movie_data['title'],
        #     director=movie_data['director'],
        #     release_date=movie_data['release_date'],
        #     # Другие поля фильма...
        # )
        # movie.save()
        
        # Возвращаем пользователю страницу с результатами
        return render(request, 'playground/movie_results.html', {'title':'Результаты поиска','movie_data': movie_data})
        # return render(request, 'movie_results.html', {'movie': movie})
    
    # Если запрос не является POST-запросом, отображаем пустую форму
    return render(request, 'playground/hello.html')