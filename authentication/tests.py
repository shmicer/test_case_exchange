from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_view(self):
        # Данные для регистрации нового пользователя
        registration_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        # Попытка регистрации нового пользователя
        response = self.client.post('/auth/register/', registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка, что пользователь добавлен в базу данных
        self.assertTrue(User.objects.filter(username=registration_data['username']).exists())

    def test_login_view(self):
        # Создаем тестового пользователя
        test_user = User.objects.create_user(username='testuser', password='testpassword')

        # Данные для входа
        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        # Попытка входа
        response = self.client.post('/auth/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка наличия токена в ответе
        self.assertTrue('access_token' in response.data)

    def test_invalid_login_view(self):
        # Данные для входа с неверными учетными данными
        invalid_login_data = {
            'username': 'nonexistentuser',
            'password': 'wrongpassword',
        }

        # Попытка входа с неверными учетными данными
        response = self.client.post('/auth/login/', invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверка, что в ответе есть ошибка
        self.assertTrue('error' in response.data)
