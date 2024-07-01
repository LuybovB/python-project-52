from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        # Создаем пользователя напрямую
        self.user = self.user_model.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            password=make_password('testpassword123')
        )
        self.initial_user_count = self.user_model.objects.count()


class TestUserCreateView(UserTestCase):
    def test_create_valid_user(self):
        user_data = {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(reverse_lazy('user-list'), data=user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(self.user_model.objects.count(), self.initial_user_count + 1)
        self.assertEqual(self.user_model.objects.last().username, user_data['username'])
