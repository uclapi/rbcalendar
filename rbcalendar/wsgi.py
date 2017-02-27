"""
WSGI config for rbcalendar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from dotenv import load_dotenv, find_dotenv
from django.core.wsgi import get_wsgi_application

load_dotenv(find_dotenv())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rbcalendar.settings")

application = get_wsgi_application()
