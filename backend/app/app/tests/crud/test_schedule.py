import pytest
from app import crud
from app.models.crontab_schedule import CrontabSchedule
from app.schemas.schedule import ScheduleCreate, ScheduleTimerCreate, ScheduleUpdate
from app.tests.utils.canvas import create_random_canvas
from app.tests.utils.crontab_schedule import random_crontab_schedule_schema
from app.tests.utils.interval_schedule import random_interval_schedule_schema
from app.tests.utils.schedule import create_random_schedule
from app.tests.utils.utils import random_lower_string
from sqlalchemy.orm import Session


@pytest.mark.parametrize(
    "schedule_timer",
    [
        pytest.param(random_interval_schedule_schema()),
        pytest.param(random_crontab_schedule_schema()),
    ],
)
def test_create_schedule(schedule_timer: ScheduleTimerCreate, db: Session) -> None:
    name = random_lower_string()
    canvas = create_random_canvas(db=db)
    obj_in = ScheduleCreate(name=name, canvas_name=canvas.name, schedule=schedule_timer)
    schedule = crud.schedule.create(db=db, obj_in=obj_in)

    assert schedule.name == name
    assert schedule.canvas == canvas

    db_schedule_timer = schedule.schedule.as_dict()
    assert db_schedule_timer.pop("id", None) is not None
    assert db_schedule_timer == schedule_timer.dict(exclude={"type"})


def test_get_schedule(db: Session) -> None:
    schedule = create_random_schedule(db)
    stored_schedule = crud.schedule.get_by_name(db=db, name=schedule.name)

    assert stored_schedule
    assert schedule.name == stored_schedule.name
    assert schedule.canvas == stored_schedule.canvas
    assert schedule.crontab == stored_schedule.crontab
    assert schedule.interval == stored_schedule.interval


def test_update_schedule(db: Session) -> None:
    schedule = create_random_schedule(db)
    schedule_timer = schedule.schedule
    schedule_crud = (
        crud.crontab_schedule
        if type(schedule_timer) is CrontabSchedule
        else crud.interval_schedule
    )

    crontab2_schema = random_crontab_schedule_schema()
    canvas2 = create_random_canvas(db)
    schedule_update = ScheduleUpdate(canvas_name=canvas2.name, schedule=crontab2_schema)

    schedule2 = crud.schedule.update(db=db, db_obj=schedule, obj_in=schedule_update)

    invalid_schedule_timer = schedule_crud.get(db=db, id=schedule_timer.id)

    assert invalid_schedule_timer is None

    assert schedule.id == schedule2.id
    assert schedule.name == schedule2.name
    assert schedule2.canvas == canvas2

    schedule2_crontab = schedule2.crontab.as_dict()
    schedule2_crontab.pop("id")
    assert schedule2_crontab == crontab2_schema.dict(exclude={"type"})


def test_remove_schedule(db: Session) -> None:
    schedule = create_random_schedule(db)
    schedule_timer = schedule.schedule
    schedule_timer_id = schedule.schedule.id
    schedule_canvas_id = schedule.canvas.id
    removed_schedule = crud.schedule.remove(db=db, id=schedule.id)
    invalid_schedule = crud.schedule.get(db=db, id=schedule.id)
    valid_canvas = crud.canvas.get(db=db, id=schedule_canvas_id)

    if type(schedule_timer) is CrontabSchedule:
        invalid_schedule_timer = crud.crontab_schedule.get(db=db, id=schedule_timer_id)
    else:
        invalid_schedule_timer = crud.interval_schedule.get(db=db, id=schedule_timer_id)

    assert invalid_schedule is None
    assert invalid_schedule_timer is None

    assert valid_canvas is not None
    assert removed_schedule == schedule


def test_remove_schedule_timer(db: Session) -> None:
    schedule = create_random_schedule(db)
    schedule_timer = schedule.schedule
    schedule_canvas_id = schedule.canvas.id
    schedule_timer_id = schedule.schedule.id

    schedule_timer_crud = (
        crud.crontab_schedule
        if type(schedule_timer) is CrontabSchedule
        else crud.interval_schedule
    )
    removed_schedule_timer = schedule_timer_crud.remove(db=db, id=schedule_timer_id)
    invalid_schedule_timer = schedule_timer_crud.get(db=db, id=schedule_timer_id)

    valid_schedule = crud.schedule.get(db=db, id=schedule.id)
    valid_canvas = crud.canvas.get(db=db, id=schedule_canvas_id)

    assert invalid_schedule_timer is None
    assert valid_schedule
    assert valid_schedule.schedule is None

    assert valid_canvas
    assert removed_schedule_timer == schedule_timer
