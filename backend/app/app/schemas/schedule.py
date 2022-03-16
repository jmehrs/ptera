from datetime import datetime
from typing import Optional, Union

from app import models
from app.models.model_base import Base
from pydantic import BaseModel, validator

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
    schedule: Optional[ScheduleTimerCreate]

    @validator("schedule", pre=True)
    def tag_schedule(cls, v):
        if isinstance(v, Base):
            if type(v) is models.CrontabSchedule:
                setattr(v, "type", "crontab")
            else:
                setattr(v, "type", "interval")
        return v


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
    interval_id: Optional[int]
    crontab_id: Optional[int]
    last_run_at: Optional[datetime]
    total_run_count: int
    date_changed: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


# Additional properties to return via API
class Schedule(ScheduleInDBBase):
    schedule: ScheduleTimer
    canvas: Canvas
