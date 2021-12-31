from fastapi import APIRouter, status, Depends
from app import schemas
from app.utils.celery import apply_async
from app.api.dependencies import get_canvas

router = APIRouter()


@router.post(
    "/",
    summary="Runs an unnamed task signature with given body parameters",
    response_description="A result id of the run task",
    response_model=schemas.TaskID,
    status_code=status.HTTP_201_CREATED,
)
def run_task(body: schemas.TaskSignature):
    result = apply_async(body.to_signature())
    task_id = schemas.TaskID(id=result.id)
    return task_id


@router.post(
    "/{canvas_name}",
    summary="Runs the canvas with the given name",
    status_code=status.HTTP_201_CREATED,
)
def run_canvas(canvas: schemas.Canvas = Depends(get_canvas)):
    result = apply_async(canvas.signature)
    task_id = schemas.TaskID(id=result.id)
    return task_id
