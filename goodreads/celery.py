import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goodreads.settings')

# Create a new Celery application instance.
app = Celery('goodreads')

# Load the celery configuration from the Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover and register task modules from all registered Django apps.
app.autodiscover_tasks()


# Define a debug task.
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
