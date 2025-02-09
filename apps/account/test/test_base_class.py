from django.urls import reverse

from rest_framework.test import APITestCase

class AccountApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse('register')
        cls.activate_url = reverse('activate')
        cls.login_url = reverse('login')
        cls.refresh_token_url = reverse('refresh-token')
        cls.logout_url = reverse('logout')
        cls.reset_password_url = reverse('reset-password')
        cls.reset_password_confirm_url = reverse('reset-password-confirm')

        cls.default_user_data = {
            'email': 'test@gmail.com',
            'first_name': 'Test',
            'last_name': 'Test',
            'password': 'pass1234',
            'password_confirm': 'pass1234',
        }
        cls.default_existing_user_data = {
            'email': 'davlyat.n@gmail.com',
            'first_name': 'Test',
            'last_name': 'Test',
            'password': 'pass1234',
            'password_confirm': 'pass1234',
        }
