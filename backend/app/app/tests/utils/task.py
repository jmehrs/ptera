from celery import signature
from celery.canvas import Signature
from .utils import random_dict, random_list
from random import choice
from app.core.celery_app import celery_tasks


def random_signature() -> Signature:
    return signature(
        choice(list(celery_tasks())),
        args=random_list(),
        kwargs=random_dict(),
        options=random_dict(),
    )
