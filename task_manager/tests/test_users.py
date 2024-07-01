from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import CustomUser
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _


class UserCRUDTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.user_model = CustomUser
        call_command('loaddata', 'users.json')
        self.initial_count = self.user_model.objects.count()

    def test_register(self):
        url = reverse('login')
        data = {
            'username': 'User4',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_user_update(self):
        call_command('loaddata', 'test_user.json')

        user = self.user_model.objects.get(pk=1)
        self.client.force_login(user)
        url = reverse('user_update', args=[user.pk])

        updated_user_data = {
            'username': 'updateduser1',
            'first_name': 'Updated',
            'last_name': 'User1',
            'password': 'pbkdf2_sha256260000'
        }

        response = self.client.post(url, updated_user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.username, updated_user_data['username'])

    def test_user_delete(self):
        user = self.user_model.objects.get(pk=1)
        self.client.force_login(user)
        url = reverse('user_delete', args=[user.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user_model.objects.filter(pk=user.pk).exists())
        self.assertEqual(self.user_model.objects.count(), self.initial_count - 1)
