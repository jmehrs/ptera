import string
from random import choice

from app import crud, models
from app.schemas import CrontabScheduleCreate
from sqlalchemy.orm import Session


def random_crontab_interval():
    return "*"


def random_crontab_schedule_schema() -> CrontabScheduleCreate:
    return CrontabScheduleCreate(
        minute=random_crontab_interval(),
        hour=random_crontab_interval(),
        day_of_week=random_crontab_interval(),
        day_of_month=random_crontab_interval(),
        month_of_year=random_crontab_interval(),
    )


def create_random_crontab_schedule(db: Session) -> models.CrontabSchedule:
    obj_in = random_crontab_schedule_schema()
    return crud.crontab_schedule.create(db=db, obj_in=obj_in)
