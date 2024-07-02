from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase
from task_manager.models import CustomUser


class UserRegistrationTest(TestCase):
    fixtures = ['users_fixture.json']

    def test_register_function(self):
        # Здесь ваш код для теста...
        # Вывод всех пользователей после загрузки фикстуры
        print(User.objects.all())

    def test_register_function(self):
        # URL для регистрации
        registration_url = reverse('register')
        # Данные для регистрации нового пользователя
        registration_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'newtestuser',
            'password': 'newpassword123',  # Используем 'password1' вместо 'password'
            'password2': 'newpassword123'
        }
        # Отправка данных на сервер
        response = self.client.post(registration_url, data=registration_data)
        # Проверка перенаправления после успешной регистрации
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)
        # Проверка, что пользователь создан
        self.assertTrue(User.objects.filter(username='newtestuser').exists())
        # Проверка, что пользователь аутентифицирован
        user = authenticate(username='newtestuser', password='newpassword123')
        self.assertIsNotNone(user)
        # Проверка сообщений об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно зарегистрирован')
