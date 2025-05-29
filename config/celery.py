import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create the Celery application
app = Celery('config')

# Use Django's settings for Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

# ADDITION: Force import specific task modules
app.autodiscover_tasks([
    'apps.integrations.coinmarketcap',
    'apps.integrations.coingecko',
])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
