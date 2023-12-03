import logging
import os

import httpx
import requests
from celery import shared_task
from django.core.cache import cache

logger = logging.getLogger(__name__)

API_KEY = os.environ.get('CURRENCY_API_KEY')


@shared_task()
def get_currency_rates_task():
    currencies = ['AED', 'USD', 'EUR', 'RUB', 'TRY', 'CNY', 'HKD']

    tasks = []

    for base in currencies:
        url = f'https://api.currencyapi.com/v3/latest?apikey={API_KEY}&base_currency={base}'
        tasks.append(fetch_currency_data(base, url))


async def fetch_currency_data(base, url):
    try:
        response = requests.get(url)
        result = response.json()['data']
        cache.set(f'{base}:currency_data', result)
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch currency data for {base}. Error: {e}")
