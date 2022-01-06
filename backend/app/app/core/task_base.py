from celery import Task
from celery.signals import task_postrun, task_prerun
from celery.utils.log import get_task_logger
from celery.worker.request import Request

logger = get_task_logger(__name__)


class MyRequest(Request):
    "A minimal custom request to log failures and hard time limits."

    def on_timeout(self, soft, timeout):
        super(MyRequest, self).on_timeout(soft, timeout)
        if not soft:
            logger.warning(f"A hard timeout was enforced for task {self.task.name}")

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        super().on_failure(
            exc_info, send_failed_event=send_failed_event, return_ok=return_ok
        )
        logger.warning(f"Failure detected for task {self.task.name}")


@task_prerun.connect
def _task_prerun(task_id, task, *args, **kwargs):
    logger.info(f"Prerun")


@task_postrun.connect
def _task_postrun(task_id, task, retval, state, *args, **kwargs):
    logger.info(f"Postrun, {retval=}, {state=}")


class DebugTask(Task):
    autoretry_for = (ArithmeticError,)
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = False

    Request = MyRequest

    def __call__(self, *args, **kwargs):
        logger.info(f"TASK STARTING: {self.name}[{self.request.id}]")
        return self.run(*args, **kwargs)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"succeeded w/ return value: {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"failed, {args = }, {kwargs = }, {einfo = }: {exc}")
