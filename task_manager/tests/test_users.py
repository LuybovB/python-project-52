from django.test import TestCase
from django.urls import reverse
from task_manager.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


class UserTests(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username='existinguser',
            password='testpassword123',
            first_name='First',
            last_name='Last',
            is_active=True
        )
        self.another_user = User.objects.create_user(
            username='anotheruser',
            password='testpassword123'
        )

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'FirstName',
            'last_name': 'LastName',
        }
        response = self.client.post(reverse('register'), data, follow=True)

        self.assertRedirects(response, reverse('login'))

        self.assertTrue(CustomUser.objects.filter(
            username='newuser', is_active=True).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]),
                         'Пользователь успешно зарегистрирован')

    def test_user_update_view(self):
        self.client.login(
            username='existinguser', password='testpassword123')
        url = reverse('user_update', kwargs={'pk': self.user.pk})

        data = {
            'username': 'updateduser',
            'password1': 'updatedpassword123',
            'password2': 'updatedpassword123',
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName'
        }

        response = self.client.post(url, data, follow=True)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'UpdatedFirstName')
        self.assertEqual(self.user.last_name, 'UpdatedLastName')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_user_delete_view_GET(self):
        self.client.login(
            username='existinguser', password='testpassword123')
        url = reverse('user_delete', kwargs={'pk': self.user.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_delete.html')

    def test_user_delete_view_POST(self):
        self.client.login(
            username='existinguser', password='testpassword123')
        url = reverse('user_delete', kwargs={'pk': self.user.pk})

        response = self.client.post(url, follow=True)

        self.assertFalse(CustomUser.objects.filter(
            username='existinguser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален.')
        self.assertRedirects(response, reverse('user-list'))

    def test_user_invalid_permissions_update(self):
        self.client.login(
            username=self.another_user.username,
            password='testpassword123'
        )
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        response = self.client.post(url, {
            'username': 'updateduser',
            'password1': 'updatedpassword123',
            'password2': 'updatedpassword123',
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName'
        })
        self.assertRedirects(response, reverse('user-list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'У вас нет прав для изменения другого пользователя.'
                         )

    def test_user_invalid_permissions_delete(self):
        self.client.login(
            username=self.another_user.username,
            password='testpassword123'
        )
        url = reverse('user_delete', kwargs={'pk': self.user.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('user-list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'У вас нет прав для изменения другого пользователя.'
                         )
