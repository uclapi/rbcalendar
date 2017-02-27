# celery -A rbcalendar worker -l info
# celery -A rbcalendar beat

from __future__ import absolute_import

import os

from celery import Celery
from core.tasks import fetch_and_cache_task, test2

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rbcalendar.settings')

from django.conf import settings  # noqa

app = Celery('rbcalendar')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600.0, fetch_and_cache_task.s())
    # sender.add_periodic_task(60.0, test2.s())


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
