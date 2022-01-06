from random import choice

from sqlalchemy.orm import Session

from app import crud, models
from app.models.crontab_schedule import CrontabSchedule
from app.schemas import ScheduleCreate

from .canvas import create_random_canvas
from .crontab_schedule import create_random_crontab_schedule
from .interval_schedule import create_random_interval_schedule
from .utils import random_lower_string


def create_random_schedule(db: Session) -> models.Schedule:
    name = random_lower_string()
    canvas = create_random_canvas(db=db)

    schedule = choice(
        (create_random_interval_schedule, create_random_crontab_schedule)
    )(db=db)

    obj_in = ScheduleCreate(name=name)

    return (
        crud.schedule.create_with_crontab
        if type(schedule) is CrontabSchedule
        else crud.schedule.create_with_interval
    )(db=db, obj_in=obj_in, canvas_id=canvas.id, schedule_id=schedule.id)
