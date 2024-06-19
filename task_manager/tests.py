from django.test import Client, TestCase
from django.urls import reverse
from .models import CustomUser
from django.shortcuts import redirect


class UserCRUDTests(TestCase):

    fixtures = ['users_fixture.json']

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.get(username='testuser')

    def test_register(self):
        url = reverse('login')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_user_update(self):
        self.client.force_login(self.user)  # Авторизуем пользователя
        url = reverse('user_update', args=[self.user.pk])
        data = {
            'username': 'updated_user',
            'email': 'updateduser@example.com'
        }
        response = self.client.post(url, data, follow=True)  # Изменили follow=True
        messages = list(response.wsgi_request._messages)

        self.assertEqual(response.status_code, 200)  # Проверяем код состояния на окончательный

    def test_user_delete(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('user_delete', args=[self.user.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 2)
