from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_view(self):

        registration_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        response = self.client.post('/auth/register/', registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(User.objects.filter(username=registration_data['username']).exists())

    def test_login_view(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')

        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        response = self.client.post('/auth/login/', login_data, format='json')
        self.assertTrue(test_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)

    def test_invalid_login_view(self):
        invalid_login_data = {
            'username': 'nonexistentuser',
            'password': 'wrongpassword',
        }

        response = self.client.post('/auth/login/', invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('error' in response.data)
