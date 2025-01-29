import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'delete_overdue_codes': {
        'task': 'apps.cart.celery_tasks.delivery_tracking',
        'schedule': 5*60,
        'args': ()
    },
}

app.conf.timezone = 'UTC'