import os
from app.core.config import settings
from celery import Celery


os.environ.setdefault('CELERY_CONFIG_MODULE', settings.CELERY_CONFIG_MODULE)

celery_app = Celery("tasks", include=['app.tasks.tasks'])
celery_app.config_from_envvar('CELERY_CONFIG_MODULE')
celery_app.conf.humanize(with_defaults=False, censored=True)