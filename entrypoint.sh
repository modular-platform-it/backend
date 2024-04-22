python manage.py migrate

python manage.py collectstatic --clear --noinput

gunicorn bot_constructor.wsgi.application --bind 0.0.0.0:8080
