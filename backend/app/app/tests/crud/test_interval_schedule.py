from random import randint

from app import crud
from app.schemas import IntervalScheduleCreate, IntervalScheduleUpdate
from app.tests.utils.interval_schedule import (
    create_random_interval_schedule,
    random_interval_period,
)
from sqlalchemy.orm import Session


def test_create_interval_schedule(db: Session) -> None:
    every = randint(1, 10)
    period = random_interval_period()
    obj_in = IntervalScheduleCreate(
        every=every,
        period=period,
    )
    interval_schedule = crud.interval_schedule.create(db=db, obj_in=obj_in)

    assert interval_schedule.every == every
    assert interval_schedule.period == period


def test_get_interval_schedule(db: Session) -> None:
    interval_schedule = create_random_interval_schedule(db)
    stored_interval_schedule = crud.interval_schedule.get(
        db=db, id=interval_schedule.id
    )

    assert stored_interval_schedule
    assert interval_schedule.every == stored_interval_schedule.every
    assert interval_schedule.period == stored_interval_schedule.period


def test_update_interval_schedule(db: Session) -> None:
    interval_schedule = create_random_interval_schedule(db)

    every2 = randint(11, 20)
    interval_schedule_update = IntervalScheduleUpdate(
        every=every2,
    )
    interval_schedule2 = crud.interval_schedule.update(
        db=db, db_obj=interval_schedule, obj_in=interval_schedule_update
    )

    assert interval_schedule.id == interval_schedule2.id
    assert interval_schedule.period == interval_schedule2.period
    assert interval_schedule2.every == every2


def test_remove_interval_schedule(db: Session) -> None:
    interval_schedule = create_random_interval_schedule(db)
    removed_interval_schedule = crud.interval_schedule.remove(
        db=db, id=interval_schedule.id
    )
    invalid_interval_schedule = crud.interval_schedule.get(
        db=db, id=interval_schedule.id
    )

    assert invalid_interval_schedule is None
    assert removed_interval_schedule
    assert removed_interval_schedule.every == interval_schedule.every
    assert removed_interval_schedule.period == interval_schedule.period
