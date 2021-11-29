from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import IntervalScheduleCreate
from app.schemas.interval_schedule import IntervalPeriods
from random import randint, choice


def random_interval_period():
    period_choices = IntervalPeriods.__args__
    return choice(period_choices)


def create_random_interval_schedule(db: Session) -> models.Canvas:
    obj_in = IntervalScheduleCreate(
        every=randint(0, 9), period=random_interval_period()
    )
    return crud.interval_schedule.create(db=db, obj_in=obj_in)
