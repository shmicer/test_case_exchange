
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Transaction
from .services import convert


class TransactionViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_transaction_create_view(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        transaction_data = {
            "currency_from": "AED",
            "currency_to": "RUB",
            "amount_from": "123.00",
            "amount_to": "3035.03",
            "exchange_rate": "24.67507",
            "timestamp": "2023-12-02T10:16:04.648148Z"
        }

        response = client.post('/api/create_transaction/', transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Transaction.objects.filter(user=self.user).exists())

    def test_transaction_list_view(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        Transaction.objects.create(
            user=self.user,
            currency_from='USD',
            currency_to='EUR',
            amount_from=50,
            amount_to=150,
            exchange_rate=3,
            timestamp="2023-12-02T10:16:04.648148Z"
        )
        Transaction.objects.create(
            user=self.user,
            currency_from='EUR',
            currency_to='USD',
            amount_from=30,
            amount_to=200,
            exchange_rate=32,
            timestamp="2023-12-02T10:16:04.648148Z"
        )

        response = client.get('/api/transactions/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), Transaction.objects.filter(user=self.user).count())

    def test_transaction_detail_view(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        transaction = Transaction.objects.create(
            user=self.user,
            currency_from='USD',
            currency_to='EUR',
            amount_from=50,
            amount_to=150,
            exchange_rate=3,
            timestamp="2023-12-02T10:16:04.648148Z"
        )

        response_get = client.get(f'/api/transactions/{transaction.id}', format='json')
        response_update = client.put(
            f'/api/transactions/{transaction.id}',
            {'currency_from': 'USD', 'currency_to': 'EUR', 'amount_from': 200},
            format='json'
        )
        response_delete = client.delete(f'/api/transactions/{transaction.id}', format='json')

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaction.objects.filter(id=transaction.id).exists())


class ConvertTestCase(TestCase):
    @patch('django.core.cache.cache.get', return_value={'EUR': {'value': 0.85}})
    def test_convert_with_cached_data(self, mock_cache_get):
        result = convert('USD', 'EUR')
        self.assertEqual(result, 0.85)
        mock_cache_get.assert_called_once_with('USD:currency_data')

    @patch('django.core.cache.cache.get', return_value=None)
    @patch('api.services.get_currency_rates_task', return_value={'EUR': {'value': 0.85}})
    def test_convert_without_cached_data(self, mock_get_currency_rates_task, mock_cache_get):
        result = convert('USD', 'EUR')
        print(result)
        self.assertEqual(result, 0.85)
        mock_cache_get.assert_called_once_with('USD:currency_data')
        mock_get_currency_rates_task.assert_called_once()
