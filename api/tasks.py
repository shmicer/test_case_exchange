import asyncio
import logging
import os

import httpx
from celery import shared_task
from django.core.cache import cache

logger = logging.getLogger(__name__)

API_KEY = os.environ.get('CURRENCY_API_KEY')


@shared_task()
async def get_currency_rates_task():
    currencies = ['AED', 'USD', 'EUR', 'RUB', 'TRY', 'CNY', 'HKD']

    async with httpx.AsyncClient() as client:
        tasks = []

        for base in currencies:
            url = f'https://api.currencyapi.com/v3/latest?apikey={API_KEY}&base_currency={base}'
            tasks.append(fetch_currency_data(client, base, url))

        await asyncio.gather(*tasks)


async def fetch_currency_data(client, base, url):
    try:
        response = await client.get(url)
        response.raise_for_status()
        result = response.json()['data']
        cache.set(f'{base}:currency_data', result)
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch currency data for {base}. Error: {e}")
