from typing import Optional, Union

from app import crud
from app.crud.crud_base import CRUDBase
from app.models import CrontabSchedule, IntervalSchedule, Schedule
from app.schemas import (
    CrontabScheduleCreate,
    IntervalScheduleCreate,
    ScheduleCreate,
    ScheduleUpdate,
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


def create_timer(
    db: Session,
    new_timer: Union[CrontabScheduleCreate, IntervalScheduleCreate],
) -> Union[CrontabSchedule, IntervalSchedule]:

    if isinstance(new_timer, CrontabScheduleCreate):
        timer = crud.crontab_schedule.create(db, obj_in=new_timer)
    else:
        timer = crud.interval_schedule.create(db, obj_in=new_timer)
    return timer


# TODO: Replace this function with a proper sqlalchemy delete-orphan relationship
#      between the schedule table and the timer tables.
def update_schedule_timer(
    db: Session,
    db_obj: Schedule,
    new_timer: Union[IntervalSchedule, CrontabSchedule],
):
    for timer_type, timer_crud, timer_model in (
        ("crontab_id", crud.crontab_schedule, CrontabSchedule),
        ("interval_id", crud.interval_schedule, IntervalSchedule),
    ):
        if old_timer_id := getattr(db_obj, timer_type, None):
            setattr(db_obj, timer_type, None)
            timer_crud.remove(db=db, id=old_timer_id)

        if isinstance(new_timer, timer_model):
            setattr(db_obj, timer_type, new_timer.id)


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Schedule]:
        return db.query(Schedule).filter(Schedule.name == name).first()

    def create(self, db: Session, *, obj_in: ScheduleCreate) -> Schedule:
        if canvas := crud.canvas.get_by_name(db, obj_in.canvas_name):
            timer = create_timer(db, new_timer=obj_in.schedule)
            if isinstance(timer, CrontabSchedule):
                schedule_id = {"crontab_id": timer.id}
            else:
                schedule_id = {"interval_id": timer.id}

            db_obj = Schedule(
                name=obj_in.name, canvas_id=canvas.id, **schedule_id
            )  # type: ignore
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

        raise ValueError(f"Canvas '{obj_in.canvas_name}' does not exist")

    def update(
        self,
        db: Session,
        *,
        db_obj: Schedule,
        obj_in: ScheduleUpdate,
    ) -> Schedule:
        obj_data = jsonable_encoder(db_obj.as_dict())
        update_data = obj_in.dict(exclude_unset=True)

        if canvas_name := obj_in.canvas_name:
            if new_canvas := crud.canvas.get_by_name(db, name=canvas_name):
                update_data["canvas_id"] = new_canvas.id
            else:
                raise ValueError(f"Canvas '{obj_in.canvas_name}' does not exist")

        if timer := obj_in.schedule:
            timer = create_timer(db, new_timer=timer)
            update_schedule_timer(db, db_obj, timer)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_by_name(self, db: Session, *, name: str) -> Optional[Schedule]:
        obj = db.query(Schedule).filter_by(name=name).one_or_none()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


schedule = CRUDSchedule(Schedule)
