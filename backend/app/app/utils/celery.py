from celery.canvas import Signature
from celery.result import AsyncResult
from fastapi import HTTPException, status


def apply_async(signature: Signature) -> AsyncResult:
    try:
        return signature.apply_async()
    except TypeError as err:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(err))
