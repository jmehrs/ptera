from typing import Literal, Optional

from celery import schedules
from pydantic import BaseModel, root_validator


# Shared properties
class CrontabScheduleBase(BaseModel):
    minute: str = "*"
    hour: str = "*"
    day_of_week: str = "*"
    day_of_month: str = "*"
    month_of_year: str = "*"

    @root_validator
    def check_cron_fmt(cls, v):
        schedules.crontab(
            minute=v["minute"],
            hour=v["hour"],
            day_of_week=v["day_of_week"],
            day_of_month=v["day_of_month"],
            month_of_year=v["month_of_year"],
        )  # Raises ValueError if bad syntax
        return v


# Properties to receive via API on creation
class CrontabScheduleCreate(CrontabScheduleBase):
    type: Literal["crontab"] = "crontab"


# Properties to receive via API on update
class CrontabScheduleUpdate(CrontabScheduleBase):
    type: Literal["crontab"] = "crontab"


class CrontabScheduleInDBBase(CrontabScheduleBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class CrontabSchedule(CrontabScheduleInDBBase):
    type: Literal["crontab"] = "crontab"
