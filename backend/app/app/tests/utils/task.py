from celery import signature
from celery.canvas import Signature
from .utils import random_dict, random_list, random_lower_string


def random_signature() -> Signature:
    return signature(
        random_lower_string(),
        args=random_list(),
        kwargs=random_dict(),
        options=random_dict(),
    )
