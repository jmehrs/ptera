from fastapi import APIRouter, Depends, status

from app import schemas
from app.api.dependencies import get_canvas
from app.models.canvas import Canvas
from app.utils.celery import apply_async

router = APIRouter()


@router.post(
    "/",
    summary="Runs an unnamed task signature with given body parameters",
    response_description="A result id of the run task",
    response_model=schemas.TaskID,
    status_code=status.HTTP_201_CREATED,
)
def run_unnamed_canvas(body: schemas.TaskSignature):
    result = apply_async(body.to_signature())
    task_id = schemas.TaskID(id=result.id)
    return task_id


@router.post(
    "/{canvas_name}",
    summary="Runs the canvas with the given name",
    status_code=status.HTTP_201_CREATED,
)
def run_named_canvas(canvas: Canvas = Depends(get_canvas)):
    result = apply_async(canvas.signature)
    task_id = schemas.TaskID(id=result.id)
    return task_id
