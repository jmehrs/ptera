from typing import List

from app import crud, models, schemas
from app.api.dependencies import get_db, get_schedule
from fastapi import APIRouter, Depends, HTTPException, Path, status
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.get(
    "/",
    summary="Returns a list of all created schedules",
    response_model=List[schemas.Schedule],
)
def get_all_schedules(
    skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
) -> List[models.Schedule]:
    schedules = crud.schedule.get_multi(db, skip=skip, limit=limit)
    return schedules


@router.post(
    "/",
    summary="Save a new schedule w/ the passed in body params to the backend store",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Schedule,
)
def create_schedule(
    schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)
) -> models.Schedule:
    try:
        return crud.schedule.create(db, obj_in=schedule)
    except IntegrityError as err:
        if type(err.orig) is UniqueViolation:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Schedule {schedule.name} already exists",
            )
        else:
            raise err
    except ValueError as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get(
    "/{schedule_name}",
    summary="Returns the specific schedule",
    response_model=schemas.Schedule,
)
def get_schedule(schedule: models.Schedule = Depends(get_schedule)) -> models.Schedule:
    return schedule


@router.patch(
    "/{schedule_name}",
    summary="Edits the celery schedule metadata",
    response_model=schemas.Schedule,
)
def edit_schedule(
    updated_schedule: schemas.CanvasUpdate,
    schedule_name: str = Path(..., title="Name of the schedule to delete"),
    db: Session = Depends(get_db),
):
    # TODO: Create
    #       crud.schedule.update_by_name(db=db, name=schedule_name, obj_in=updated_canvas)
    ...


@router.delete(
    "/{schedule_name}",
    summary="Removes schedule from backend store",
    response_model=schemas.Schedule,
)
def delete_schedule(
    schedule_name: str = Path(..., title="Name of the schedule to delete"),
    db: Session = Depends(get_db),
) -> models.Schedule:
    if schedule := crud.schedule.remove_by_name(db, name=schedule_name):
        return schedule
    else:
        raise HTTPException(
            status_code=404, detail=f"Schedule '{schedule_name}' not found"
        )
