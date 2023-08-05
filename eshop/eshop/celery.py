"""Celery configuration settings."""

import os
from celery import Celery

# Set the default Django settings module for the 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")

app = Celery('eshop')

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
