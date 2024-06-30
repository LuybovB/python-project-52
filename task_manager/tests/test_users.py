from django.test import Client, TestCase
from django.urls import reverse
from task_manager.models import CustomUser


class UserCRUDTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user, created = CustomUser.objects.get_or_create(
            username='testuser',
            defaults={'password': 'testpass'}
        )

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

        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        initial_count = CustomUser.objects.count()  # Сохраняем исходное количество пользователей
        self.client.login(username='testuser', password='testpass')  # Используйте правильный пароль
        url = reverse('user_delete', args=[self.user.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        new_count = CustomUser.objects.count()  # Получаем новое количество пользователей
        self.assertEqual(new_count, initial_count - 1)  # Проверяем, что количество уменьшилось на одного

