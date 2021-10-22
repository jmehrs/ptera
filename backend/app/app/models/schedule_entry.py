import json
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

from app.models.model_base import Base
from app.models.crontab_schedule import CrontabSchedule
from app.models.interval_schedule import IntervalSchedule


class ScheduleEntry(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    task = Column(String(255))
    interval_id = Column(Integer, ForeignKey('intervalschedule.id'))
    crontab_id = Column(Integer, ForeignKey('crontabschedule.id'))
    arguments = Column(String(255), default='[]')
    keyword_arguments = Column(String(255), default='{}')
    queue = Column(String(255))
    exchange = Column(String(255))
    routing_key = Column(String(255))
    expires = Column(DateTime)
    enabled = Column(Boolean, default=True)
    last_run_at = Column(DateTime)
    total_run_count = Column(Integer, default=0)
    date_changed = Column(DateTime)

    interval = relationship(IntervalSchedule)
    crontab = relationship(CrontabSchedule)

    @property
    def args(self):
        return json.loads(self.arguments)

    @args.setter
    def args(self, value):
        self.arguments = json.dumps(value)

    @property
    def kwargs(self):
        return json.loads(self.keyword_arguments)

    @kwargs.setter
    def kwargs(self, kwargs_):
        self.keyword_arguments = json.dumps(kwargs_)

    @property
    def schedule(self):
        if self.interval:
            return self.interval.schedule
        if self.crontab:
            return self.crontab.schedule