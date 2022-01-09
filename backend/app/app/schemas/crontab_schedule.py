from typing import Literal, Optional

from pydantic.main import BaseModel


# Shared properties
class CrontabScheduleBase(BaseModel):
    minute: Optional[str] = None
    hour: Optional[str] = None
    day_of_week: Optional[str] = None
    day_of_month: Optional[str] = None
    month_of_year: Optional[str] = None


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
    pass
