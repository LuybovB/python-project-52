from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import CustomUser, Task, Status, Label


class TaskViewTests(TestCase):

    fixtures = ['users_fixture.json']

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.executor = CustomUser.objects.create_user(
            username='executor',
            password='execpass'
        )
        self.status = Status.objects.create(name='Тестовый статус')
        self.label = Label.objects.create(name='Срочно')
        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Тестовое описание',
            status=self.status,
            author=self.user,
            executor=self.executor
        )
        self.client.force_login(self.user)

    def test_task_list_view(self):
        url = reverse('task_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')

    def test_task_create_view(self):
        url = reverse('task_create')
        data = {
            'name': 'Новая задача',
            'description': 'Новое описание',
            'status': self.status.id,
            'executor': self.executor.id,
            'labels': [self.label.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(
            name='Новая задача').exists())

    def test_task_update_view(self):
        url = reverse('task_update', args=[self.task.id])
        data = {
            'name': 'Обновленная задача',
            'description': 'Обновленное описание',
            'status': self.status.id,
            'executor': self.executor.id,
            'labels': [self.label.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(
            name='Обновленная задача').exists())
