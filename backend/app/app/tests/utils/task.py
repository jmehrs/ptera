from random import choice

from celery import signature
from celery.canvas import Signature

from app.core.celery_app import celery_tasks

from .utils import random_dict, random_list

good_bare_minimum_task = {
    "task": "test.ping",
}

good_complex_task = {
    "task": "celery.chain",
    "subtask_type": "chain",
    "kwargs": {
        "tasks": [
            {
                "task": "test.echo",
                "args": ["echo "],
            },
            {
                "task": "test.echo",
                "args": ["echo "],
            },
            {
                "task": "celery.chord",
                "subtask_type": "chord",
                "kwargs": {
                    "header": [
                        {
                            "task": "test.echo",
                            "args": ["echo "],
                        },
                        {
                            "task": "test.echo",
                            "args": ["echo "],
                        },
                        {
                            "task": "test.echo",
                            "args": ["echo "],
                        },
                    ],
                    "body": {
                        "task": "test.echo",
                        "args": ["echo "],
                    },
                },
            },
        ]
    },
}

bad_unregistered_task = {
    "task": "test.non_existant",
    "options": {"eta": 5, "timeout": 60},
}

bad_malformed_task = {
    "oops": "Not even a canvas",
    "spilled": ["Not", "even", "a", "canvas"],
    "my": {"macaroni": "with", "the": "nuggets"},
    "beans": 42,
}


def random_signature() -> Signature:
    return signature(
        choice(list(celery_tasks())),
        args=random_list(),
        kwargs=random_dict(),
        options=random_dict(),
    )
