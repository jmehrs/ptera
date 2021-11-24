from celery import states
from celery.canvas import Signature
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status, Depends
from app import crud, models, schemas
from app.core import celery_app
from app.api.dependencies import get_task_signature
from app.schemas import TaskSignature
from typing import Optional, TYPE_CHECKING, Union


router = APIRouter()


@router.post(
    "/task",
    summary="Runs the task with given body parameters",
    response_description="A result id of the run task",
    response_model=schemas.TaskID,
    status_code=status.HTTP_201_CREATED,
)
def run_task(task_signature: Signature = Depends(get_task_signature)):
    result = task_signature.apply_async()
    task_id = schemas.TaskID(id=result.id)
    return task_id


@router.post(
    "/canvas",
    summary="Runs the canvas with given body parameters",
    status_code=status.HTTP_201_CREATED,
)
def run_canvas():
    ...
