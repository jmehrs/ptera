from random import choice

from app import crud, models
from app.schemas import ScheduleCreate
from sqlalchemy.orm import Session

from .canvas import create_random_canvas
from .crontab_schedule import random_crontab_schedule_schema
from .interval_schedule import random_interval_schedule_schema
from .utils import random_lower_string


def create_random_schedule(db: Session, *, enabled=False) -> models.Schedule:
    name = random_lower_string()
    canvas = create_random_canvas(db=db)

    schedule = choice(
        (random_interval_schedule_schema(), random_crontab_schedule_schema())
    )

    obj_in = ScheduleCreate(
        name=name, enabled=enabled, canvas_name=canvas.name, schedule=schedule
    )

    return crud.schedule.create(db=db, obj_in=obj_in)
