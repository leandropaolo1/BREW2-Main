from core.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, REDIS_PASSWORD, REDIS_USERNAME
from datetime import timedelta
from celery import Celery
import uuid
import ssl
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
if REDIS_USERNAME and REDIS_PASSWORD:
    app = Celery(
        "core",
        broker_connection_retry_on_startup=True,
        backend=CELERY_RESULT_BACKEND,
        broker=CELERY_BROKER_URL,
        broker_use_ssl={
            'ssl_cert_reqs': ssl.CERT_REQUIRED
        },
        redis_backend_use_ssl={
            'ssl_cert_reqs': ssl.CERT_REQUIRED
        })
else:
    app = Celery(
        "core",
        broker_connection_retry_on_startup=True,
        backend=CELERY_RESULT_BACKEND,
        broker=CELERY_BROKER_URL)


app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'generate-proforma': {
        'task': 'Proformas.tasks.generate_proforma',
        'schedule': timedelta(seconds=10),
        'args': (True,),
        'options': {'task_id': f"{uuid.uuid4()}"}
    },
    'generate-purchase': {
        'task': 'Purchases.tasks.generate_purchase',
        'schedule': timedelta(seconds=10),
        'args': (True,),
        'options': {'task_id': f"{uuid.uuid4()}"}
    },
}
