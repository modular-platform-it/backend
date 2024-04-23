python manage.py migrate

python manage.py collectstatic --clear --noinput

gunicorn --bind 0:8000 bot_constructor.wsgi.application
