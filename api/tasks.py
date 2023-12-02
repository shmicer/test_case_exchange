from celery import shared_task
import requests
import os

from django.core.cache import cache


API_KEY = os.environ.get('CURRENCY_API_KEY')


@shared_task()
def get_currency_rates_task():
    currencies = ['AED', 'USD', 'EUR', 'RUB', 'TRY', 'CNY', 'HKD']
    for base in currencies:
        try:
            url = f'https://api.currencyapi.com/v3/latest?apikey={API_KEY}&base_currency={base}'
            response = requests.get(url).json()
            result = response['data']
            cache.set(f'{base}:currency_data', result)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch currency data for {base}. Error: {e}")

