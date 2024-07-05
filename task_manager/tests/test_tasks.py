from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from task_manager.models import Task, Status, Label

User = get_user_model()


class TaskTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1', password='testpassword123')
        self.user2 = User.objects.create_user(
            username='testuser2', password='testpassword456')
        self.status = Status.objects.create(name='InitialStatus')
        self.label = Label.objects.create(name='bug')
        self.task = Task.objects.create(
            name='Test Task',
            status=self.status,
            author=self.user1,
            description='This is a test task',
        )

    def test_task_create_view_with_login(self):
        self.client.login(
            username='testuser1', password='testpassword123')
        data = {
            'name': 'New Task',
            'status': self.status.pk,
            'description': 'New task description',
            'label': [self.label.pk]
        }
        response = self.client.post(
            reverse('task_create'), data, follow=True)
        self.assertRedirects(response, reverse('task_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_create_view_without_login(self):
        response = self.client.get(reverse('task_create'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('task_create')}")

    def test_task_update_view_with_login(self):
        self.client.login(
            username='testuser1', password='testpassword123')
        data = {
            'name': 'Updated Task',
            'status': self.status.pk,
            'description': 'Updated task description',
            'label': [self.label.pk]
        }
        response = self.client.post(
            reverse('task_update',
                    kwargs={'pk': self.task.pk}), data, follow=True)
        self.assertRedirects(response, reverse('task_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), 'Задача успешно изменена')

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_detail_view_with_login(self):
        self.client.login(
            username='testuser1', password='testpassword123')
        response = self.client.get(
            reverse('task_detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_delete_view_with_login(self):
        self.client.login(
            username='testuser1', password='testpassword123')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': self.task.pk}), follow=True)
        self.assertRedirects(response, reverse('task_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_view_as_non_author(self):
        self.client.login(username='testuser2', password='testpassword456')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': self.task.pk}), follow=True)
        self.assertRedirects(response, reverse('task_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]),
                         'Задачу может удалить только ее автор')

        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
