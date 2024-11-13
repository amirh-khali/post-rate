import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_rate.settings')

app = Celery('post_rate')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def debug_task(self):
    print(f'Request: {self.request!r}')