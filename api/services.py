from django.core.cache import cache

from api.tasks import get_currency_rates_task


def convert(from_currency, to_currency):
    data_key = f'{from_currency}:currency_data'
    if data_key in cache:
        data = cache.get(data_key)
    else:
        get_currency_rates_task()
        data = cache.get(data_key)
    result = data[to_currency]['value']
    return result
