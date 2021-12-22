from typing import Any, Dict, Optional, Union
from fastapi.encoders import jsonable_encoder
from pydantic.errors import CallableError

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from .crontab_schedule import crontab_schedule
from .interval_schedule import interval_schedule


def remove_old_periods(
    db: Session,
    old_obj: Dict[str, Any],
    db_obj: Schedule,
):
    for period_id, period_crud in (
        ("crontab_id", crontab_schedule),
        ("interval_id", interval_schedule),
    ):
        if old_obj[period_id] is not None:
            period_crud.remove(db=db, id=old_obj[period_id])
            setattr(db_obj, period_id, None)


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Schedule]:
        return db.query(Schedule).filter(Schedule.name == name).first()

    def create_with_interval(
        self, db: Session, *, obj_in: ScheduleCreate, canvas_id: int, schedule_id: int
    ) -> Schedule:
        db_obj = Schedule(
            name=obj_in.name, canvas_id=canvas_id, interval_id=schedule_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_crontab(
        self, db: Session, *, obj_in: ScheduleCreate, canvas_id: int, schedule_id: int
    ) -> Schedule:
        db_obj = Schedule(name=obj_in.name, canvas_id=canvas_id, crontab_id=schedule_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Schedule,
        obj_in: Union[ScheduleUpdate, Dict[str, Any]],
    ) -> Schedule:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                if (
                    field in ("crontab_id", "interval_id")
                    and obj_data[field] != update_data[field]
                ):
                    remove_old_periods(db, obj_data, db_obj)
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


schedule = CRUDSchedule(Schedule)
