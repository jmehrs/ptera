from celery import schedules
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from app.models.model_base import Base


class CrontabSchedule(Base):
    id = Column(Integer, primary_key=True)
    minute = Column(String(64), default="*")
    hour = Column(String(64), default="*")
    day_of_week = Column(String(64), default="*")
    day_of_month = Column(String(64), default="*")
    month_of_year = Column(String(64), default="*")

    @property
    def schedule(self):
        return schedules.crontab(
            minute=self.minute,
            hour=self.hour,
            day_of_week=self.day_of_week,
            day_of_month=self.day_of_month,
            month_of_year=self.month_of_year,
        )

    @classmethod
    def from_schedule(cls, dbm, schedule):
        spec = {
            "minute": schedule._orig_minute,
            "hour": schedule._orig_hour,
            "day_of_week": schedule._orig_day_of_week,
            "day_of_month": schedule._orig_day_of_month,
            "month_of_year": schedule._orig_month_of_year,
        }
        try:
            query = dbm.query(CrontabSchedule)
            query = query.filter_by(**spec)
            existing = query.one()
            return existing
        except NoResultFound:
            return cls(**spec)
        except MultipleResultsFound:
            query = dbm.query(CrontabSchedule)
            query = query.filter_by(**spec)
            query.delete()
            dbm.commit()
            return cls(**spec)
