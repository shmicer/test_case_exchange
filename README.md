# Web-приложение для обмена валюты

В приложении реализована регистрация и аутентификация пользователей с помощью JWT токенов.
История операций сохраняется в базе данных для каждого пользователя.


- На данный момент доступно 7 валют для конвертации: ['AED', 'USD', 'EUR', 'RUB', 'TRY', 'CNY', 'HKD'].
- Курсы валют запрашиваются со стороннего сервиса https://currencyapi.com/ раз в сутки с помощью Celery
- Чтобы уменьшить число запросов к стороннему сервису, полученные данные кэшируются с помощью Redis.
- 

Стек используемых технологий:
* Django Rest Framework
* Docker
* Docker-compose
* PostgreSQL
* Redis
* Celery

### Регистрация пользователей:

На вход по URL auth/register/ POST запросом передаются данные такого вида:

```json
{
    "username": "value1",
    "password": "value2"
}

```

В ответ возвращается словарь из refresh и access токенов для авторизации

```json
{
    "refresh": "value1",
    "access": "value2"
}

```

### Конвертация валюты

На вход по URL api/create_transaction/ POST запросом передаются данные такого вида:

```json
{
    "currency_from": "CNY",
    "currency_to": "EUR",
    "amount_from": 150
}

```

При успешном выполнении запроса транзакция записывается в базу данных

### Просмотр истории конвертаций

При выполнении GET запроса по URL api/transactions/ в ответе выдается список со всеми транзакциями.

```json
[
{
  "id": 7,
  "currency_from": "AED",
  "currency_to": "RUB",
  "amount_from": "123.00",
  "amount_to": "3035.03",
  "exchange_rate": "24.67507",
  "timestamp": "2023-12-02T10:16:04.648148Z"
}
]
```

### Просмотр, изменение, удаление транзакции

При выполнении GET запроса по URL api/transactions/{id} в ответе выдается информация по транзакции вида:

```json
{
    "id": 31,
    "currency_from": "AED",
    "currency_to": "EUR",
    "amount_from": "100.00",
    "amount_to": "1.02",
    "exchange_rate": "0.01015",
    "timestamp": "2023-12-02T15:24:15.701525Z"
}
```
Для изменения данных о транзакции необходимо выполнить PUT запрос по URL api/transactions/{id}, указав в теле запроса новые данные:

```json
{
    "currency_from": "new_value1",
    "currency_to": "new_value2",
    "amount_from": "new_value3"
}
```

Для удаления транзакции необходимо выполнить DELETE запрос по URL api/transactions/{id}

