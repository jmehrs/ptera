from contextlib import closing
from typing import Generator

from celery.app.task import Task
from celery.result import AsyncResult
from fastapi import Depends, HTTPException, Path
from sqlalchemy.orm.session import Session

from app import crud
from app.core import celery_app
from app.db.session import SessionLocal
from app.models.canvas import Canvas


def get_db() -> Generator:
    with closing(SessionLocal()) as db:
        yield db


def get_task_info(task_name: str = Path(..., title="Name of the task to get")) -> Task:

    if (task := celery_app.tasks.get(task_name)) is None:
        raise HTTPException(status_code=404, detail=f"Task '{task_name}' not found")
    else:
        return task


def get_task_result(
    task_id: str = Path(..., title="The result id to query")
) -> AsyncResult:
    result = AsyncResult(id=task_id)
    return result


def get_canvas(
    canvas_name: str = Path(..., title="The Canvas to retrieve"),
    db: Session = Depends(get_db),
) -> Canvas:

    if canvas := crud.canvas.get_by_name(db, canvas_name):
        return canvas
    else:
        raise HTTPException(status_code=404, detail=f"Canvas '{canvas_name}' not found")
