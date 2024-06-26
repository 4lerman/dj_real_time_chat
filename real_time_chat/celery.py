from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_time_chat.settings')

# Create an instance of the Celery application.
app = Celery('real_time_chat')

# Load any custom configuration from Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed applications.
app.autodiscover_tasks()
