from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import CustomUser, Label


class LabelCRUDTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.get(username='testuser1')
        self.client.force_login(self.user)
        self.initial_label = Label.objects.get(name='urgent')

    def test_create_label(self):
        new_label_data = {'name': 'label1'}
        response = self.client.post(reverse('label_create'), new_label_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='label1').exists())

    def test_update_label(self):
        label_id = self.initial_label.id
        updated_label_data = {'name': 'label2'}
        response = self.client.post(reverse('label_update', args=[label_id]), updated_label_data)

        self.assertEqual(response.status_code, 302)
        self.initial_label.refresh_from_db()
        self.assertEqual(self.initial_label.name, 'label2')

    def test_delete_label(self):
        label_id = self.initial_label.id
        response = self.client.post(reverse('label_delete', args=[label_id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=label_id).exists())
