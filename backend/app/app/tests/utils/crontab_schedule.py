import string
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import CrontabScheduleCreate
from random import choice


def random_crontab_interval():
    interval_choices = string.digits + "*"
    return choice(interval_choices)


def create_random_crontab_schedule(db: Session) -> models.CrontabSchedule:
    obj_in = CrontabScheduleCreate(
        minute=random_crontab_interval(),
        hour=random_crontab_interval(),
        day_of_week=random_crontab_interval(),
        day_of_month=random_crontab_interval(),
        month_of_year=random_crontab_interval(),
    )
    return crud.crontab_schedule.create(db=db, obj_in=obj_in)
