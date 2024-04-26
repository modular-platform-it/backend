python manage.py migrate --noinput

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

python manage.py collectstatic --clear --noinput

gunicorn --bind 0.0.0.0:8000 bot_constructor.bot_constructor.wsgi:application
