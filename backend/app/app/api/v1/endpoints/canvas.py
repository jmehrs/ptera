from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter
from app import crud, models, schemas
from app.core import celery_app
from typing import Optional, TYPE_CHECKING, Union

router = APIRouter()


@router.get("/", summary="Returns a list of all created canvases")
def get_all_canvases():
    ...


@router.post(
    "/",
    summary="Creates the celery canvas function and stores it in the database",
)
def create_canvas(canvas: schemas.CanvasCreate):
    ...


@router.get(
    "/{canvas_name}", summary="Returns more detailed information about a canvas"
)
def get_canvas():
    ...


@router.patch(
    "/{canvas_name}",
    summary="Edits the celery canvas metadata",
)
def edit_canvas():
    ...


@router.delete(
    "/{canvas_name}",
    summary="Removes canvas from backend store",
)
def delete_canvas():
    ...
