from decouple import config
from .base import *  # noqa: F403
import os

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")
CELERY_TIMEZONE = config("CELERY_TIMEZONE", default="UTC")


#Debugging
print("CELERY_BROKER_URL:", CELERY_BROKER_URL)