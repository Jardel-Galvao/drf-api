from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamarcado.settings.dev')

app = Celery('tamarcado', broker='redis://localhost/0', backend='redis://localhost/0')
default_config = 'tamarcado.celeryconfig'
app.config_from_object(default_config)

app.autodiscover_tasks()

@app.task
def soma(a,b):
    return a + b