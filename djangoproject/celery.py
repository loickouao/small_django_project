from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

import django

import dotenv
#If you are using Django, you should add the above loader script at the top of wsgi.py and manage.py.
dotenv.load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
)

# for run django before celery // task django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
django.setup()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

app = Celery('djangoproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(force=True)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

