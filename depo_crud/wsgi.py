import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "depo_crud.settings.production")

application = get_wsgi_application()
