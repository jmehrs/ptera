from app.api.dependencies import get_task_result
from celery.exceptions import NotRegistered
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.get("/{task_id}", summary="Returns the results of the specified task-id")
def get_result(result: AsyncResult = Depends(get_task_result)):
    if result.ready():
        try:
            return result.get()
        except NotRegistered as err:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Result unavailable. {err!r} Valid tasks can be found by "
                    "performing a GET request on the /tasks path."
                ),
            )

    raise HTTPException(
        status.HTTP_202_ACCEPTED, detail="The result is still processing"
    )
