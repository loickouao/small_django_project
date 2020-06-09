#from _future_ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

import django

# for run django before celery // task django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
django.setup()

_all_ = ('celery_app',)
