from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter
from app import crud, models, schemas
from app.core import celery_app
from typing import Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from celery.result import EagerResult
    from celery.app.task import Task

router = APIRouter()

def update_response_result(response, result):
    response['result'] = result.result
    if result.state == states.FAILURE:
        response['traceback'] = result.traceback

@router.get(
    "/registered",
    summary="Get all tasks",
)
async def get_tasks(attributes: Optional[str]=None):
    # TODO: *args for query parameter
    tasks = celery_app.control.inspect().registered(attributes or '')
    return {"message": "Success", 'data': tasks}

@router.post(
    "/run/{task_name}",
    summary="run task",
)
async def run_async_task(task_name: str, params: schemas.TaskArgs):
    try:
        task: Task = celery_app.tasks[task_name]
    except KeyError:
        return # TODO: Return 404 task not found

    result: EagerResult = task.apply_async(
        args=params.args, kwargs=params.kwargs, **params.run_options
    )

    return {"task_id": result.task_id}

@router.get(
    "/query",
    summary="Returns details on the running task(s)",
)
async def get_task_details(task_ids: Optional[str]=None):
    # TODO: *args for query parameter
    details = celery_app.control.inspect().query_task(task_ids or '')
    return {"message": f"running task: {details}"}

@router.get(
    "/result/{task_id}",
    summary="Get the specified unit",
)
async def get_task_result(task_id: str, timeout: Union[float, int, None] = None):
    timeout = float(timeout) if timeout is not None else None
    try:
        result = AsyncResult(task_id)
    except ValueError:
        return # TODO: Return 404 task_id not found

    response = {"task_id": result.task_id, "state": result.state}
    
    if timeout:
        result.get(timeout=timeout, propagate=False)
        update_response_result(response, result)
    elif result.ready():
        update_response_result(response, result)

    return response