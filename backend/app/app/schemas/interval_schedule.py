from typing import Literal, Optional

from pydantic.main import BaseModel

# Valid Interval periods
IntervalPeriods = Literal[
    "days", "seconds", "microseconds", "milliseconds", "minutes", "hours", "weeks"
]


# Shared properties
class IntervalScheduleBase(BaseModel):
    every: Optional[int] = None
    period: Optional[IntervalPeriods] = None


# Properties to receive via API on creation
class IntervalScheduleCreate(IntervalScheduleBase):
    type: Literal["interval"] = "interval"
    every: int
    period: Optional[IntervalPeriods] = None


# Properties to receive via API on update
class IntervalScheduleUpdate(IntervalScheduleBase):
    type: Literal["interval"] = "interval"


class IntervalScheduleInDBBase(IntervalScheduleBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class IntervalSchedule(IntervalScheduleInDBBase):
    pass
