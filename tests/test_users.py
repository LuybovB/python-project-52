from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from django.contrib.messages import get_messages

User = get_user_model()


class UserRegistrationTest(TestCase):
    def test_register_function(self):
        # URL для регистрации
        registration_url = reverse('register')
        # Данные для регистрации нового пользователя
        registration_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'newtestuser',
            'password': 'newpassword123',
            'password2': 'newpassword123'
        }
        # Отправка данных на сервер
        response = self.client.post(registration_url, data=registration_data)
        # Проверка перенаправления после успешной регистрации
        self.assertEqual(response.status_code, 302)
        # Проверка, что пользователь создан
        self.assertTrue(User.objects.filter(username='newtestuser').exists())
        # Проверка, что пользователь аутентифицирован
        user = authenticate(username='newtestuser', password='newpassword123')
        self.assertIsNotNone(user)
        # Проверка сообщений об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно зарегистрирован')
