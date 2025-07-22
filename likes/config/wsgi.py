import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likes.config.settings.main')

application = get_wsgi_application()
