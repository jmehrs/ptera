from typing import Any

from celery import Celery
from celery.result import AsyncResult


def run_task(celery: Celery, **options: Any) -> AsyncResult:
    return celery.tasks["test.ping"].apply_async(**options)
