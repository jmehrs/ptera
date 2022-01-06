import json
from typing import Any, Dict, Union

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

from .canvas import Canvas
from .crontab_schedule import CrontabSchedule
from .interval_schedule import IntervalSchedule
from .model_base import Base


class Schedule(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    canvas_id = Column(Integer, ForeignKey("canvas.id"))
    interval_id = Column(
        Integer,
        ForeignKey("intervalschedule.id"),
    )
    crontab_id = Column(
        Integer,
        ForeignKey("crontabschedule.id"),
    )
    enabled = Column(Boolean, default=True)
    last_run_at = Column(DateTime)
    total_run_count = Column(Integer, default=0)
    date_changed = Column(DateTime)

    canvas = relationship(Canvas)
    interval = relationship(
        IntervalSchedule,
        backref="schedule",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    crontab = relationship(
        CrontabSchedule,
        backref="schedule",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    @property
    def schedule(self) -> Union[IntervalSchedule, CrontabSchedule]:
        if self.interval:
            return self.interval
        else:
            return self.crontab

    @staticmethod
    def dict_to_json(signature: Dict[str, Any]) -> str:
        return json.dumps(signature)
