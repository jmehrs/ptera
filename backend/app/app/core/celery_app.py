import os
from typing import Set

from celery import Celery

from app.core.config import settings

os.environ.setdefault("CELERY_CONFIG_MODULE", settings.CELERY_CONFIG_MODULE)

celery_app = Celery("tasks", include=["app.tasks.tasks"])
celery_app.config_from_envvar("CELERY_CONFIG_MODULE")
celery_app.conf.humanize(with_defaults=False, censored=True)


def celery_tasks() -> Set:
    return set(celery_app.tasks)
