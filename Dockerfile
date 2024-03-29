FROM python:3.12-slim

EXPOSE 80

WORKDIR /app

COPY ./requirements /requirements

RUN pip install --no-cache-dir --upgrade -r /requirements/production.txt

COPY . /app

CMD DATABASE_URL=$DATABASE_URL SITE_HOST=$SITE_HOST DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY uvicorn config.asgi:application --host 0.0.0.0 --port 80
