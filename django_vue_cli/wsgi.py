"""
WSGI config for  task.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# set the DJANGO_SETTINGS_MODULE environment variable to the settings.py file in django_vue_cli module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_vue_cli.settings")

application = get_wsgi_application()
