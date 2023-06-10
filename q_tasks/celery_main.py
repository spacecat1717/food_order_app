from celery import Celery

from q_tasks.settings.main import CELERY_BACKEND_URL, CELERY_BROKER_URL

celery_main = Celery(__name__, backend=CELERY_BACKEND_URL, broker=CELERY_BROKER_URL)
