from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamarcado.settings.dev')

app = Celery('tamarcado')
app.conf.broker_url = 'redis://127.0.0.1:6379/0'

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()

@app.task
def soma(a,b):
    return a + b