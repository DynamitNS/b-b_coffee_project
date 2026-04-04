from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


User = get_user_model()


class AuthPagesTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page_available(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вход')

    def test_register_page_available(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Регистрация')

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@test.ru',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertIn('_auth_user_id', self.client.session)
