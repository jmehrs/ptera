from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter
from app import crud, models, schemas
from app.core import celery_app
from typing import Optional, TYPE_CHECKING, Union

router = APIRouter()


@router.get("/", summary="Returns a list of all created schedules")
def get_all_schedules():
    ...


@router.post(
    "/",
    summary="Save a new schedule w/ the passed in body params to the backend store",
)
def create_schedule():
    ...


@router.get(
    "/{schedule_name}", summary="Returns more detailed information about a schedule"
)
def get_schedule():
    ...


@router.patch(
    "/{schedule_name}",
    summary="edits the celery schedule metadata",
)
def edit_schedule(schedule_name: str, schedule: str):
    ...


@router.delete(
    "/{schedule_name}",
    summary="Removes schedule from backend store",
)
def delete_schedule():
    ...
