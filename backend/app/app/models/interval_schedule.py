from app.models.model_base import Base
from sqlalchemy import Column, Integer, String


class IntervalSchedule(Base):
    id = Column(Integer, primary_key=True)
    every = Column(Integer, nullable=False)
    period = Column(String(24))

    # @property
    # def schedule(self):
    #     return schedules.schedule(timedelta(**{self.period: self.every}))

    # @classmethod
    # def from_schedule(cls, dbsession, schedule, period="seconds"):
    #     every = max(schedule.run_every.total_seconds(), 0)
    #     try:
    #         query = dbsession.query(IntervalSchedule)
    #         query = query.filter_by(every=every, period=period)
    #         existing = query.one()
    #         return existing
    #     except NoResultFound:
    #         return cls(every=every, period=period)
    #     except MultipleResultsFound:
    #         query = dbsession.query(IntervalSchedule)
    #         query = query.filter_by(every=every, period=period)
    #         query.delete()
    #         dbsession.commit()
    #         return cls(every=every, period=period)
