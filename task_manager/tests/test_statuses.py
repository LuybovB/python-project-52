from django.test import Client, TestCase
from django.urls import reverse
from task_manager.models import CustomUser, Status


class UserCRUDTests(TestCase):

    fixtures = ['users_fixture.json']

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.status = Status.objects.create(name='Тестовый статус')

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('create_status'),
            {'name': 'Новый статус'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Новый статус').exists())

    def test_update_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('update_status',
                    args=[self.status.id]),
            {'name': 'Обновленный статус'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Обновленный статус')

    def test_delete_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete_status', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(
            name='Тестовый статус').exists()
                         )
