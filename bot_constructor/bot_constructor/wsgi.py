import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_constructor.bot_constructor.settings")

application = get_wsgi_application()
