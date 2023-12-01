FROM python:3.12:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add --no-cache python3-dev openssl-dev libffi-dev gcc

RUN pip install --upgrade pip
COPY requirements /requirements
RUN pip install -r /requirements/local.txt

WORKDIR /app

CMD python manage.py migrate \
    && python manage.py runserver 0.0.0.0:8000