from django.urls import path
from . import views

urlpatterns = [
    path('exmple/', views.test_text, name='home'),
    path('hello/', views.say_hello, name='greetings'),
    path('main_page/', views.main_page, name='main page'),
    path('create/', views.create, name='create'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('update/<int:id>/', views.update, name='update'),
    path('about_us/', views.wir, name='about us'),
    path('movie_results/', views.search_movie, name='movie results')

]