from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from playground.models import Films, Films_Cost
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
    # Получаем данные из моделей Films и Films_Cost
    films = Films.objects.all()
    films_cost = Films_Cost.objects.all()

    # Передаем данные в контекст шаблона
    context = {
        'films': films,
        'films_cost': films_cost,
    }

    # Рендерим шаблон с переданным контекстом
    return render(request, 'registration/profile.html', context)