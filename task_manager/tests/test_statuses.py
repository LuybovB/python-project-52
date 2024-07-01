from django.test import TestCase
from django.urls import reverse
from task_manager.models import CustomUser, Status
from django.test import Client


class StatusCRUDTests(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.get(username='testuser1')

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('create_status'),
            {'name': 'New_status'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New_status').exists())

    def test_update_status(self):
        self.client.force_login(self.user)
        status_to_update = Status.objects.get(pk=1)
        response = self.client.post(
            reverse('update_status', args=[status_to_update.pk]),
            {'name': 'All_finished'}
        )
        self.assertEqual(response.status_code, 302)
        status_to_update.refresh_from_db()
        self.assertEqual(status_to_update.name, 'All_finished')

    def test_delete_status(self):
        self.client.force_login(self.user)
        status_to_delete = Status.objects.get(pk=1)
        response = self.client.post(
            reverse('delete_status', args=[status_to_delete.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=status_to_delete.pk).exists())