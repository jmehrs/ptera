from typing import List

from celery import Task
from fastapi import APIRouter
from fastapi.param_functions import Depends

from app import schemas
from app.api.dependencies import get_task_info
from app.core import celery_app

router = APIRouter()


@router.get("/", summary="Returns a list of all tasks", response_model=List[str])
def get_task_list(skip: int = 0, limit: int = 50):
    tasks = sorted(celery_app.tasks.keys())
    return tasks[skip : skip + limit]


@router.get(
    "/{task_name}",
    summary="Returns more detailed information about a task",
    response_model=schemas.TaskConfig,
)
def get_task_info(task: Task = Depends(get_task_info)):
    # TODO: Check if the task config actually updates when app broadcasts changes to tasks.
    # TODO: Create endpoint to broadcast changes to task config
    # https://docs.celeryproject.org/en/stable/userguide/workers.html#remote-control

    task_config = schemas.TaskConfig.from_task(task)
    return task_config


# TODO: Future work
# @router.patch(
#     "/{task_name}",
#     summary="Updates the specified task's metadata with the given body parameters",
# )
# def edit_task(task_name: str):
#     ...
