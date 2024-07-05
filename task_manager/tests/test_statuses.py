from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from task_manager.models import Status, Task

User = get_user_model()


class StatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.status = Status.objects.create(name='InitialStatus')

    def test_create_status_without_login(self):
        response = self.client.get(reverse('create_status'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('create_status')}"
        )

    def test_create_status_with_login(self):
        self.client.login(username='testuser', password='testpassword123')
        data = {'name': 'NewStatus'}

        response = self.client.post(
            reverse('create_status'), data, follow=True)
        self.assertRedirects(response, reverse('list_statuses'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

        self.assertTrue(Status.objects.filter(name='NewStatus').exists())

    def test_update_status_without_login(self):
        response = self.client.get(reverse('update_status',
                                           kwargs={'pk': self.status.pk}))
        self.assertRedirects(
            response,
            f"{reverse('login')}"
            f"?next={reverse('update_status',kwargs={'pk': self.status.pk})}"
        )

    def test_update_status_with_login(self):
        self.client.login(username='testuser', password='testpassword123')
        data = {'name': 'UpdatedStatus'}

        response = self.client.post(reverse('update_status',
                                            kwargs={'pk': self.status.pk}),
                                    data, follow=True)
        self.assertRedirects(response, reverse('list_statuses'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), 'Статус успешно изменен')

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'UpdatedStatus')

    def test_delete_status_without_login(self):
        response = self.client.get(reverse('delete_status',
                                           kwargs={'pk': self.status.pk}))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next="
            f"{reverse('delete_status',kwargs={'pk': self.status.pk})}"
        )

    def test_delete_status_with_login(self):
        self.client.login(username='testuser', password='testpassword123')

        response = self.client.post(reverse(
            'delete_status', kwargs={'pk': self.status.pk}), follow=True)
        self.assertRedirects(response, reverse('list_statuses'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_delete_status_in_use(self):

        self.client.login(username='testuser', password='testpassword123')

        Task.objects.create(
            name='Test Task',
            status=self.status,
            author=self.user,
            description='This is a test task'
        )

        response = self.client.post(reverse(
            'delete_status', kwargs={'pk': self.status.pk}), follow=True)
        self.assertRedirects(response, reverse('list_statuses'))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]),
                         'Невозможно удалить статус,'
                         ' потому что он используется')

        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
