from typing import Optional, Union

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime

from .canvas import Canvas
from .crontab_schedule import (
    CrontabSchedule,
    CrontabScheduleCreate,
    CrontabScheduleUpdate,
)
from .interval_schedule import (
    IntervalSchedule,
    IntervalScheduleCreate,
    IntervalScheduleUpdate,
)

ScheduleTimerUpdate = Union[CrontabScheduleUpdate, IntervalScheduleUpdate]
ScheduleTimerCreate = Union[CrontabScheduleCreate, IntervalScheduleCreate]
ScheduleTimer = Union[CrontabSchedule, IntervalSchedule]


# Shared properties
class ScheduleBase(BaseModel):
    name: Optional[str] = None
    enabled: Optional[bool] = None
    canvas_name: Optional[Canvas] = None
    schedule: Optional[ScheduleTimer]


# Properties to receive via API on creation
class ScheduleCreate(ScheduleBase):
    name: str
    enabled: bool = True
    canvas_name: str
    schedule: ScheduleTimerCreate


# Properties to receive via API on update
class ScheduleUpdate(ScheduleBase):
    enabled: Optional[bool] = None
    canvas_name: Optional[str] = None
    schedule: Optional[ScheduleTimerCreate] = None


class ScheduleInDBBase(ScheduleBase):
    id: int
    name: str
    enabled: bool
    canvas_id: int
    interval_id: int
    crontab_id: int
    last_run_at: DateTime
    total_run_count: int
    date_changed: DateTime

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


# Additional properties to return via API
class Schedule(ScheduleInDBBase):
    canvas: Canvas
