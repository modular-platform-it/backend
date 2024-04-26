cd /app/bot_constructor/

# python manage.py migrate

# python manage.py collectstatic --clear --noinput

gunicorn --bind 0.0.0.0:8000 bot_constructor.wsgi
