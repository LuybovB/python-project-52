from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import CustomUser, Task, Status, Label
from task_manager.read_json import load_data


class TaskViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Загрузите фикстуры здесь
        cls.fixtures = ['users.json', 'statuses.json', 'tasks.json']
        cls.user = CustomUser.objects.get(username='testuser1')
        cls.status = Status.objects.get(name='New')
        cls.executor = CustomUser.objects.create(
            username='executor',
            first_name='Executor',
            last_name='User',
            password='pbkdf2_sha256260000'
        )
        cls.label = Label.objects.create(name='urgent')
        cls.task = Task.objects.create(
            name='Task1',
            description='Description for Task1',
            status=cls.status,
            creator=cls.user,
            executor=cls.executor
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_task_list_view(self):
        self.client.force_login(self.user)
        url = reverse('task_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_create_view(self):
        self.client.force_login(self.user)
        url = reverse('task_create')
        response = self.client.post(url, self.test_task_data['create'])
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name=self.test_task_data['create']['name']).exists())

    def test_task_update_view(self):
        self.client.force_login(self.user)
        url = reverse('task_update', args=[self.task.id])
        response = self.client.post(url, self.test_task_data['update'])
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, self.test_task_data['update']['name'])

    def test_task_delete_view(self):
        self.client.force_login(self.user)
        task_to_delete = Task.objects.get(name='Task1')

        self.assertTrue(Task.objects.filter(pk=task_to_delete.pk).exists())

        url = reverse('task_delete', args=[task_to_delete.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task_to_delete.pk).exists())
        self.assertRedirects(response, reverse('task_list'))

        # Logout and login as executor, as additional check
        self.client.logout()
        self.client.force_login(self.executor)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)  # Resource no longer exists