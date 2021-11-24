from typing import Generator
from celery.app.task import Task
from celery.result import AsyncResult

from fastapi import HTTPException, Path

from app.db.session import SessionLocal
from app.schemas import TaskSignature
from celery.canvas import Signature
from app.core import celery_app


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_task_info(task_name: str = Path(..., title="Name of the task to get")) -> Task:

    if (task := celery_app.tasks.get(task_name)) is None:
        raise HTTPException(status_code=404, detail=f"Task '{task_name}' not found")
    else:
        return task


def get_task_signature(body: TaskSignature) -> Signature:

    if (task := celery_app.tasks.get(body.task)) is None:
        raise HTTPException(status_code=404, detail=f"Task '{body.task}' not found")
    else:
        return Signature(body.dict())


def get_task_result(
    task_id: str = Path(..., title="The result id to query")
) -> AsyncResult:
    result = AsyncResult(id=task_id)
    return result
