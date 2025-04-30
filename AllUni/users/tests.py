from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTests(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'StrongPass123',
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_register_user_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'NewStrongPass123',
            'password2': 'NewStrongPass123',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registrar")

    def test_login_user_post_success(self):
        response = self.client.post(reverse('login'), {
            'username': self.credentials['username'],
            'password': self.credentials['password'],
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_user_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'wrong',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor")  

    def test_login_user_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar")

    def test_logout_user(self):
        self.client.login(**self.credentials)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
 
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')

    def test_dashboard_authenticated(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.credentials['username'])
