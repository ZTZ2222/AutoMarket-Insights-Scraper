import os
from celery import Celery

celery = Celery("celery", broker=os.getenv("CELERY_BROKER_URL"))
