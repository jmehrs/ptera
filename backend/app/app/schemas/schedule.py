from typing import Optional

from pydantic.main import BaseModel
from sqlalchemy.sql.sqltypes import DateTime

from .canvas import Canvas
from .crontab_schedule import CrontabSchedule
from .interval_schedule import IntervalSchedule


# Shared properties
class ScheduleBase(BaseModel):
    name: Optional[str] = None
    enabled: bool = False


# Properties to receive via API on creation
class ScheduleCreate(ScheduleBase):
    name: str


# Properties to receive via API on update
class ScheduleUpdate(ScheduleBase):
    enabled: Optional[bool] = None
    canvas_id: Optional[int] = None
    interval_id: Optional[int] = None
    crontab_id: Optional[int] = None


class ScheduleInDBBase(ScheduleBase):
    id: Optional[int] = None
    canvas_id: Optional[int] = None
    interval_id: Optional[int] = None
    crontab_id: Optional[int] = None
    last_run_at: Optional[DateTime] = None
    total_run_count: Optional[int] = None
    date_changed: Optional[DateTime] = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


# Additional properties to return via API
class Schedule(ScheduleInDBBase):
    canvas: Canvas
    crontab: Optional[CrontabSchedule] = None
    interval: Optional[IntervalSchedule] = None
