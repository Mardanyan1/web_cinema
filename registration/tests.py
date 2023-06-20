from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class ResponseTest(TestCase):
    #проверяем работоспособность страниц
    def test_main(self):
        response = self.client.get('/registration/register/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/registration/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/registration/logout/')
        self.assertEqual(response.status_code, 302)


class RegistrationTest(TestCase):
    def test_registration(self):
        # Создаем данные для регистрации
        username = 'testuser'
        email = 'example@mail.com'
        password = 'testpassword'
        # Формируем URL для страницы регистрации
        url = reverse('register')
        # Отправляем POST-запрос с данными регистрации
        response = self.client.post(url, 
                                    {'username': username, 
                                     'email': email, 
                                     'password1': password, 
                                     'password2': password})
        # Проверяем, что пользователь успешно зарегистрирован
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление после успешной регистрации
        self.assertTrue(User.objects.filter(username=username).exists())  # Проверяем, что пользователь создан
        # Проверяем, что пользователь может войти после регистрации
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': username, 'password': password})
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление после успешного входа


