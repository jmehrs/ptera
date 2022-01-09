from random import choice, randint

from app import crud, models
from app.schemas import IntervalScheduleCreate
from app.schemas.interval_schedule import IntervalPeriods
from sqlalchemy.orm import Session


def random_interval_period():
    period_choices = IntervalPeriods.__args__
    return choice(period_choices)


def random_interval_schedule_schema() -> IntervalScheduleCreate:
    return IntervalScheduleCreate(every=randint(0, 9), period=random_interval_period())


def create_random_interval_schedule(db: Session) -> models.IntervalSchedule:
    obj_in = random_interval_schedule_schema()
    return crud.interval_schedule.create(db=db, obj_in=obj_in)
