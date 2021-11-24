from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from app import crud, models, schemas
from app.core import celery_app
from app.api.dependencies import get_task_result
from typing import Optional, TYPE_CHECKING, Union


router = APIRouter()


@router.get("/{task_id}", summary="Returns the results of the specified task-id")
def get_result(result: AsyncResult = Depends(get_task_result)):
    if result.ready():
        return result.get()

    return HTTPException(
        status.HTTP_202_ACCEPTED, detail="The result is still processing"
    )
