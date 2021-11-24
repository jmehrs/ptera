from celery import states
from celery import Task
from celery.result import AsyncResult
from fastapi import APIRouter, Path
from fastapi.param_functions import Depends
from app import crud, models, schemas
from app.core import celery_app
from app.api.dependencies import get_task_info
from typing import List, Optional, TYPE_CHECKING, Union

router = APIRouter()


@router.get("/", summary="Returns a list of all tasks", response_model=List[str])
def get_task_list(skip: int = 0, limit: int = 50):
    tasks = sorted(celery_app.tasks.keys())
    public_tasks = [task for task in tasks if not task.startswith("celery.")]
    return public_tasks[skip : skip + limit]


@router.get(
    "/{task_name}",
    summary="Returns more detailed information about a task",
    response_model=schemas.TaskConfig,
)
def get_task_info(task: Task = Depends(get_task_info)):

    task_config = schemas.TaskConfig.from_task(task)
    return task_config


# TODO: Future work
# @router.patch(
#     "/{task_name}",
#     summary="Updates the specified task's metadata with the given body parameters",
# )
# def edit_task(task_name: str):
#     ...
