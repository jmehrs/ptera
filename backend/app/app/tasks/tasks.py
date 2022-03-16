import errno
import time
from random import choice, randint
from typing import Any, Collection, Iterable, Union

from app.core import celery_app
from app.core.task_base import DebugTask
from celery.exceptions import Reject
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
number = Union[int, float]


@celery_app.task(bind=True, base=DebugTask, default_retry_delay=3)
def badadd(self, x: number, y: number) -> number:
    try:
        if randint(0, 1):
            raise ArithmeticError("BAD ADD")
        return x + y
    except ArithmeticError as err:
        raise self.retry(exc=err)


@celery_app.task(
    base=DebugTask,
    autoretry_for=(ArithmeticError,),
    retry_kwargs={"max_retries": 3},
    default_retry_delay=3,
)
def neat_badadd(x: number, y: number) -> number:
    if randint(0, 1):
        raise ArithmeticError("BAD ADD")
    return x + y


@celery_app.task(name="tasks.add", base=DebugTask)
def add(x: number, y: number) -> number:
    return x + y


@celery_app.task
def mul(x: number, y: number) -> number:
    return x * y


@celery_app.task
def xsum(numbers: Iterable[number]) -> number:
    return sum(numbers)


@celery_app.task(bind=True)
def upload_files(self, filenames):
    for i, file in enumerate(filenames):
        if not self.request.called_directly:
            time.sleep(3)
            self.update_state(
                state="PROGRESS", meta={"current": i, "total": len(filenames)}
            )


@celery_app.task(bind=True, acks_late=True, ignore_results=True)
def render_scene(self, path):
    exc = choice((MemoryError, OSError, Exception))
    try:
        raise exc
    # if the file is too big to fit in memory
    # we reject it so that it's redelivered to the dead letter exchange
    # and we can manually inspect the situation.
    except MemoryError as exc:
        raise Reject(exc, requeue=False)
    except OSError as exc:
        if exc.errno == errno.ENOMEM:
            raise Reject(exc, requeue=False)
    # For any other error we retry after 10 seconds.
    except Exception as exc:
        raise self.retry(exc, countdown=10)


# PERIODIC
# @celery_app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
# Calls test('hello') every 10 seconds.
# sender.add_periodic_task(10.0, add.s(2,5), name='add every 10 seconds')

# Calls test('hello') every 10 minutes.
# sender.add_periodic_task(crontab(minute='*/10'), add.s(2,5), name='add every 10 minutes')

# Executes every Monday morning at 7:30 a.m.
# sender.add_periodic_task(
#     crontab(hour=7, minute=30, day_of_week=1),
#     test.s('Happy Mondays!'),
# )

# HELPERS


def on_raw_message(body):
    print(body)


@celery_app.task(name="test.echo", base=DebugTask)
def echo(*args: Any) -> Collection[Any]:
    return args


@celery_app.task(name="test.ping", base=DebugTask)
def ping() -> str:
    return "pong"
