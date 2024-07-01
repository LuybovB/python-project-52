from django.test import Client, TestCase
from django.urls import reverse
from .models import CustomUser, Status
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

class UserCRUDTests(TestCase):

    def create_users(db):
        User = get_user_model()
        User.objects.create_user(username='user1', password='testpass123')
        User.objects.create_user(username='user2', password='testpass123')
        User.objects.create_user(username='user3', password='testpass123')

    def test_load_users(create_users):
        users = get_user_model().objects.all()
        assert len(users) == 3

    fixtures = ['users_fixture.json']

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.get(username='testuser')
        self.status = Status.objects.create(name='Тестовый статус')

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
        self.client.force_login(self.user)
        url = reverse('user_update', args=[self.user.pk])
        data = {
            'username': 'updated_user',
            'email': 'updateduser@example.com'
        }
        response = self.client.post(url, data, follow=True)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('user_delete', args=[self.user.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 2)


    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_status'), {'name': 'Новый статус'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Новый статус').exists())

    def test_update_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('update_status', args=[self.status.id]), {'name': 'Обновленный статус'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Обновленный статус')

    def test_delete_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_status', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(name='Тестовый статус').exists())