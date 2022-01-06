from sqlalchemy.orm import Session

from app import crud
from app.models.crontab_schedule import CrontabSchedule
from app.schemas import ScheduleCreate, ScheduleUpdate
from app.tests.utils.canvas import create_random_canvas
from app.tests.utils.crontab_schedule import create_random_crontab_schedule
from app.tests.utils.interval_schedule import create_random_interval_schedule
from app.tests.utils.schedule import create_random_schedule
from app.tests.utils.utils import random_lower_string


def test_create_interval_schedule(db: Session) -> None:
    name = random_lower_string()
    canvas = create_random_canvas(db=db)
    interval = create_random_interval_schedule(db=db)

    obj_in = ScheduleCreate(name=name)
    schedule = crud.schedule.create_with_interval(
        db=db, obj_in=obj_in, canvas_id=canvas.id, schedule_id=interval.id
    )

    assert schedule.name == name
    assert schedule.canvas == canvas
    assert schedule.interval == interval


def test_create_crontab_schedule(db: Session) -> None:
    name = random_lower_string()
    canvas = create_random_canvas(db=db)
    crontab = create_random_crontab_schedule(db=db)

    obj_in = ScheduleCreate(name=name)
    schedule = crud.schedule.create_with_crontab(
        db=db, obj_in=obj_in, canvas_id=canvas.id, schedule_id=crontab.id
    )

    assert schedule.name == name
    assert schedule.canvas == canvas
    assert schedule.crontab == crontab


def test_get_schedule(db: Session) -> None:
    schedule = create_random_schedule(db)
    stored_schedule = crud.schedule.get(db=db, id=schedule.id)

    assert stored_schedule
    assert schedule.name == stored_schedule.name
    assert schedule.canvas == stored_schedule.canvas
    assert schedule.crontab == stored_schedule.crontab
    assert schedule.interval == stored_schedule.interval


def test_update_schedule(db: Session) -> None:
    schedule = create_random_schedule(db)
    schedule_period = schedule.schedule
    invalid_schedule_crud = (
        crud.crontab_schedule
        if type(schedule_period) is CrontabSchedule
        else crud.interval_schedule
    )

    crontab2 = create_random_crontab_schedule(db)
    canvas2 = create_random_canvas(db)
    schedule_update = ScheduleUpdate(canvas_id=canvas2.id, crontab_id=crontab2.id)

    schedule2 = crud.schedule.update(db=db, db_obj=schedule, obj_in=schedule_update)

    invalid_schedule_period = invalid_schedule_crud.get(db=db, id=schedule_period.id)

    assert invalid_schedule_period is None

    assert schedule.id == schedule2.id
    assert schedule.name == schedule2.name
    assert schedule2.canvas == canvas2
    assert schedule2.crontab == crontab2


def test_remove_schedule(db: Session) -> None:
    schedule = create_random_schedule(db)
    schedule_period = schedule.schedule
    schedule_period_id = schedule.schedule.id
    schedule_canvas_id = schedule.canvas.id
    removed_schedule = crud.schedule.remove(db=db, id=schedule.id)
    invalid_schedule = crud.schedule.get(db=db, id=schedule.id)
    valid_canvas = crud.canvas.get(db=db, id=schedule_canvas_id)

    removed_schedule_period = (
        crud.crontab_schedule
        if type(schedule_period) is CrontabSchedule
        else crud.interval_schedule
    ).get(db=db, id=schedule_period_id)

    assert invalid_schedule is None
    assert removed_schedule_period is None

    assert valid_canvas is not None
    assert removed_schedule == schedule


def test_remove_schedule_period(db: Session) -> None:
    schedule = create_random_schedule(db)
    schedule_period = schedule.schedule
    schedule_canvas_id = schedule.canvas.id
    schedule_period_id = schedule.schedule.id

    schedule_period_crud = (
        crud.crontab_schedule
        if type(schedule_period) is CrontabSchedule
        else crud.interval_schedule
    )
    removed_schedule_period = schedule_period_crud.remove(db=db, id=schedule_period_id)
    invalid_schedule_period = schedule_period_crud.get(db=db, id=schedule_period_id)

    valid_schedule = crud.schedule.get(db=db, id=schedule.id)
    valid_canvas = crud.canvas.get(db=db, id=schedule_canvas_id)

    assert invalid_schedule_period is None
    assert valid_schedule
    assert valid_schedule.schedule is None

    assert valid_schedule is not None
    assert valid_canvas is not None
    assert removed_schedule_period == schedule_period
