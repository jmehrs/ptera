import json
from typing import Any, Dict
from celery import signature as signature_
from celery.canvas import Signature
from celery.schedules import BaseSchedule
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

from .crontab_schedule import CrontabSchedule
from .interval_schedule import IntervalSchedule
from .model_base import Base, JSONBType


class CanvasScheduleEntry(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    signature = Column(JSONBType)
    interval_id = Column(Integer, ForeignKey("intervalschedule.id"))
    crontab_id = Column(Integer, ForeignKey("crontabschedule.id"))
    enabled = Column(Boolean, default=True)
    last_run_at = Column(DateTime)
    total_run_count = Column(Integer, default=0)
    date_changed = Column(DateTime)

    interval = relationship(IntervalSchedule)
    crontab = relationship(CrontabSchedule)

    @property
    def sig(self) -> Signature:
        json_signature = json.loads(self.signature)
        return signature_(json_signature)

    @sig.setter
    def sig(self, value: Signature) -> None:
        self.signature = json.dumps(value)

    @property
    def schedule(self) -> BaseSchedule:
        if self.interval:
            return self.interval.schedule
        if self.crontab:
            return self.crontab.schedule

    def sig_to_dict(self) -> Dict[str, Any]:
        return json.loads(self.signature)

    @staticmethod
    def dict_to_json(signature: Dict[str, Any]) -> str:
        return json.dumps(signature)
