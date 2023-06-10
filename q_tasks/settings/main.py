import os

from dotenv import load_dotenv

load_dotenv()

CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
