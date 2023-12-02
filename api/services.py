from django.core.cache import cache

from api.tasks import get_currency_rates_task


def convert(from_currency, to_currency):
    if f'{from_currency}:currency_data' in cache:
        data = cache.get(f'{from_currency}:currency_data')
    else:
        data = get_currency_rates_task()
    result = data[to_currency]['value']
    return result
