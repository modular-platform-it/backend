import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_server.settings")

app = Celery("bot_server")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
