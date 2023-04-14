from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import Like_filmsForm
from .models import Like_films



def test_text(request):
    like_films = Like_films.objects.all()
    return render(request, 'playground/exmple.html',  {'title':'ТЕСТОВАЯ', 'like_films':like_films})

def say_hello(request):
    return render(request, 'playground/hello.html', {'name':'Artyom','title':'Hello User'})


def main_page(request):
    like_films = Like_films.objects.all()
    return render(request, 'playground/main_page.html', {'title':'Главная страница', 'like_films':like_films})


def wir(request):
    return render(request, 'playground/about_us.html', {'title':'О нас'})


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


def delete(request, id):
    obj = get_object_or_404(Like_films, id=id)
    if request.method == "POST" and request.POST.get("delete"):
        obj.delete()
        return redirect('greetings')
    context = {
        'object': obj,
        'title':'Delete'
    }
    return render(request, "playground/delete.html", context)


def update(request, id):
    like_films = get_object_or_404(Like_films, id=id)
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