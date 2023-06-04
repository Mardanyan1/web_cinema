import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from playground.models import Films, Films_Cost, Like_films
from .forms import UserRegisterForm
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/playgroung/hello')

@login_required
def profile(request):
    # current_user = request.user
    # like_films = Like_films.objects.filter(user=current_user)
    # like_films_ids = like_films.values_list('id_filmRequest', flat=True)

    # films_cost = Films_Cost.objects.filter(id_filmRequest__in=like_films_ids)
    # films_cost_ids = films_cost.values_list('id_film', flat=True)
    # print("-------------")
    # print(films_cost)

    # films = Films.objects.all()
    # films = Films_Cost.objects.filter(id_film__in=films_cost)
    # print("-------------")
    # print(films)









    current_user = request.user
    like_films = Like_films.objects.filter(user=current_user)
    like_films_ids = like_films.values_list('id_filmRequest', flat=True)

    films_cost = Films_Cost.objects.filter(id_filmRequest__in=like_films_ids)
    films_cost_ids = films_cost.values_list('id_film', flat=True)

    films = Films.objects.filter(id_film__in=films_cost_ids)

    films_data = []

    for film in films:
        film_data = {
            'film_name': film.film_name,
            'image': film.photo,
            'year': film.year
        }

        film_costs = Films_Cost.objects.filter(id_film=film)

        cost_data = {}
        for i, film_cost in enumerate(film_costs):
            cost_data[str(i)] = {
                'link': film_cost.link,
                'viewing_method': film_cost.viewing_method,
                'quality': film_cost.quality,
                'price': film_cost.cost
            }

        film_data.update(cost_data)

        films_data.append(film_data)

    json_data = json.dumps(films_data)
    print(json_data)
    json_data = json.loads(json_data)
    print("-------------")
    print(json_data)

    return render(request, 'registration/profile.html', {'films_data': json_data})
    # Рендерим шаблон с переданным контекстом
    return render(request, 'registration/profile.html', context)