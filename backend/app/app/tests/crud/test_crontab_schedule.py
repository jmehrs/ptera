from sqlalchemy.orm import Session

from app import crud
from app.schemas import CrontabScheduleCreate, CrontabScheduleUpdate
from app.tests.utils.crontab_schedule import (
    create_random_crontab_schedule,
    random_crontab_interval,
)


def test_create_crontab_schedule(db: Session) -> None:
    minute = random_crontab_interval()
    hour = random_crontab_interval()
    day_of_week = random_crontab_interval()
    day_of_month = random_crontab_interval()
    month_of_year = random_crontab_interval()
    obj_in = CrontabScheduleCreate(
        minute=minute,
        hour=hour,
        day_of_week=day_of_week,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
    )
    crontab_schedule = crud.crontab_schedule.create(db=db, obj_in=obj_in)

    assert crontab_schedule.minute == minute
    assert crontab_schedule.hour == hour
    assert crontab_schedule.day_of_week == day_of_week
    assert crontab_schedule.day_of_month == day_of_month
    assert crontab_schedule.month_of_year == month_of_year


def test_get_crontab_schedule(db: Session) -> None:
    crontab_schedule = create_random_crontab_schedule(db)
    stored_crontab_schedule = crud.crontab_schedule.get(db=db, id=crontab_schedule.id)

    assert stored_crontab_schedule
    assert crontab_schedule.minute == stored_crontab_schedule.minute
    assert crontab_schedule.hour == stored_crontab_schedule.hour
    assert crontab_schedule.day_of_week == stored_crontab_schedule.day_of_week
    assert crontab_schedule.day_of_month == stored_crontab_schedule.day_of_month
    assert crontab_schedule.month_of_year == stored_crontab_schedule.month_of_year


def test_update_crontab_schedule(db: Session) -> None:
    crontab_schedule = create_random_crontab_schedule(db)

    hour2 = random_crontab_interval()
    day_of_week2 = random_crontab_interval()
    day_of_month2 = random_crontab_interval()
    month_of_year2 = random_crontab_interval()
    crontab_schedule_update = CrontabScheduleUpdate(
        hour=hour2,
        day_of_week=day_of_week2,
        day_of_month=day_of_month2,
        month_of_year=month_of_year2,
    )
    crontab_schedule2 = crud.crontab_schedule.update(
        db=db, db_obj=crontab_schedule, obj_in=crontab_schedule_update
    )

    assert crontab_schedule.id == crontab_schedule2.id
    assert crontab_schedule.minute == crontab_schedule2.minute
    assert crontab_schedule2.day_of_week == day_of_week2
    assert crontab_schedule2.day_of_month == day_of_month2
    assert crontab_schedule2.month_of_year == month_of_year2


def test_delete_crontab_schedule(db: Session) -> None:
    crontab_schedule = create_random_crontab_schedule(db)
    removed_crontab_schedule = crud.crontab_schedule.remove(
        db=db, id=crontab_schedule.id
    )
    invalid_crontab_schedule = crud.crontab_schedule.get(db=db, id=crontab_schedule.id)

    assert invalid_crontab_schedule is None
    assert removed_crontab_schedule.id == crontab_schedule.id
    assert removed_crontab_schedule.minute == crontab_schedule.minute
    assert removed_crontab_schedule.hour == crontab_schedule.hour
    assert removed_crontab_schedule.day_of_week == crontab_schedule.day_of_week
    assert removed_crontab_schedule.day_of_month == crontab_schedule.day_of_month
    assert removed_crontab_schedule.month_of_year == crontab_schedule.month_of_year
