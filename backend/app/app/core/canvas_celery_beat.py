from __future__ import annotations
import datetime
import numbers
import sys
import time
import traceback
from typing import Any, Dict, Optional, Tuple, Union
from celery import schedules, current_app
from celery.app.base import Celery
from celery.beat import Scheduler, ScheduleEntry, SchedulingError
from celery.exceptions import reraise
from celery.schedules import BaseSchedule, schedstate as SchedState
from celery.utils.log import get_logger
from celery.utils.time import is_naive
from sqlalchemy.orm import scoped_session
from kombu import Producer

from app.db.session import SessionLocal
from app.models.canvas_schedule_entry import CanvasScheduleEntry
from app.models.crontab_schedule import CrontabSchedule
from app.models.interval_schedule import IntervalSchedule


dbsession = scoped_session(SessionLocal)

logger = get_logger(__name__)
debug, info, error, warning = (logger.debug, logger.info, logger.error, logger.warning)

ScheduleModel = Union[CrontabSchedule, IntervalSchedule]


class CanvasEntry(ScheduleEntry):
    model_schedules = (
        (schedules.crontab, CrontabSchedule, "crontab"),
        (schedules.schedule, IntervalSchedule, "interval"),
    )

    def __init__(self, model: CanvasScheduleEntry) -> None:
        self.app = current_app._get_current_object()
        self.name = model.name
        self.signature = model.signature
        self.sig = model.sig  # Actual Celery signature object
        self.schedule = model.schedule
        self.total_run_count = model.total_run_count
        self.model = model

        if not model.last_run_at:
            model.last_run_at = self._default_now()
        orig = self.last_run_at = model.last_run_at
        if not is_naive(self.last_run_at):
            self.last_run_at = self.last_run_at.replace(tzinfo=None)
        assert orig.hour == self.last_run_at.hour  # timezone sanity

    def is_due(self) -> SchedState:
        if not self.model.enabled:
            return False, 5.0  # 5 second delay for re-enable.
        return self.schedule.is_due(self.last_run_at)

    def _default_now(self) -> datetime.datetime:
        return datetime.datetime.utcnow()

    def __next__(self) -> CanvasEntry:
        self.model.last_run_at = self._default_now()
        self.model.total_run_count += 1
        dbsession.commit()
        return self.__class__(self.model)

    next = __next__  # for 2to3

    def __reduce__(self) -> Tuple[CanvasEntry, Tuple]:
        return self.__class__, (
            self.name,
            self.signature,
            self.last_run_at,
            self.total_run_count,
            self.schedule,
        )

    def __repr__(self) -> str:
        return "<{name}: {0.name} {0.schedule}".format(self, name=type(self).__name__)

    def editable_fields_equal(self, other: CanvasEntry) -> bool:
        for attr in ("signature", "schedule"):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __eq__(self, other: CanvasEntry) -> bool:
        """Test schedule entries equality.

        Will only compare "editable" fields:
        ``task``, ``schedule``, ``args``, ``kwargs``, ``options``.
        """
        return self.editable_fields_equal(other)

    @classmethod
    def to_model_schedule(
        cls, schedule: Union[numbers.Number, datetime.timedelta, BaseSchedule]
    ) -> Tuple[ScheduleModel, str]:
        for schedule_type, model_type, model_field in cls.model_schedules:
            schedule = schedules.maybe_schedule(schedule)
            if isinstance(schedule, schedule_type):
                model_schedule = model_type.from_schedule(dbsession, schedule)
                return model_schedule, model_field
        raise ValueError("Cannot convert schedule type {0!r} to model".format(schedule))

    @classmethod
    def from_entry(
        cls,
        name: str,
        skip_fields: Optional[Tuple[str]] = None,
        **entry: Dict[str, Any],
    ) -> CanvasEntry:
        fields = dict(entry)
        for skip_field in skip_fields or ():
            fields.pop(skip_field, None)

        schedule = fields.pop("schedule")
        signature = fields.pop("signature")
        model_schedule, model_field = cls.to_model_schedule(schedule)
        model_signature = CanvasScheduleEntry.dict_to_json(signature)
        fields[model_field] = model_schedule
        fields["signature"] = model_signature

        query = dbsession.query(CanvasScheduleEntry)
        query = query.filter_by(name=name)
        db_entry = query.first()
        if db_entry is None:
            new_entry = CanvasScheduleEntry(**fields)
            new_entry.name = name
            dbsession.add(new_entry)
            dbsession.commit()
            db_entry = new_entry
        return cls(db_entry)


class CanvasDatabaseScheduler(Scheduler):
    Entry = CanvasEntry
    Schedules = Dict[str, Entry]
    _last_timestamp = None
    _initial_read = False
    _schedule: Schedules = {}

    def __init__(self, app: Celery, **kwargs) -> None:
        self._last_timestamp = self._get_latest_change()
        Scheduler.__init__(self, app, **kwargs)

    def _get_latest_change(self) -> datetime.datetime:
        query = dbsession.query(CanvasScheduleEntry.date_changed)
        query = query.order_by(CanvasScheduleEntry.date_changed.desc())
        latest_entry_date = query.first()
        return latest_entry_date

    def schedule_changed(self) -> bool:
        ts = self._get_latest_change()

        if ts and ts[0] and ts > self._last_timestamp:
            self._last_timestamp = ts
            return True
        return False

    def setup_schedule(self) -> None:
        self.install_default_entries(self.schedule)
        self.update_from_dict(self.app.conf.CELERYBEAT_SCHEDULE)

    def _all_as_schedule(self) -> Schedules:
        s = {}
        query = dbsession.query(CanvasScheduleEntry)
        query = query.filter_by(enabled=True)
        for row in query:
            s[row.name] = self.Entry(row)
        return s

    def update_from_dict(self, dict_: Dict[str, Any]) -> None:
        s = {}
        for name, entry in dict_.items():
            try:
                s[name] = self.Entry.from_entry(name, **entry)
            except Exception as exc:
                self.logger.exception(
                    f"update_from_dict: could not, update canvas entry {name}"
                )
        self.schedule.update(s)

    @property
    def schedule(self) -> Schedules:
        update = False
        if not self._initial_read:
            self.logger.debug("DatabaseScheduler: intial read")
            update = True
            self._initial_read = True
        elif self.schedule_changed():
            self.logger.info("DatabaseScheduler: Schedule changed.")
            update = True

        if update:
            self.sync()
        return self._schedule

    def sync(self) -> None:
        self._last_sync = time.time()
        self.logger.debug("DatabaseScheduler: sync")
        self._schedule = self._all_as_schedule()

    def tick(self) -> int:
        self.logger.debug("DatabaseScheduler: tick")
        Scheduler.tick(self)
        if self.should_sync():
            self.sync()
        return 1  # sleep time until next tick

    def should_sync(self) -> bool:
        sync_reason_time = (time.time() - self._last_sync) > self.sync_every
        sync_reason_task_count = (
            self.sync_every_tasks and self._tasks_since_sync >= self.sync_every_tasks
        )
        bool_ = sync_reason_time or sync_reason_task_count
        self.logger.debug("DatabaseScheduler: should_sync: {0}".format(bool_))
        return bool_

    def apply_entry(self, entry: Entry, producer: Optional[Producer] = None) -> None:
        info("Scheduler: Sending due signature %s (%s)", entry.name, entry.signature)
        try:
            result = self.apply_async(entry, producer=producer, advance=False)
        except Exception as exc:  # pylint: disable=broad-except
            error("Message Error: %s\n%s", exc, traceback.format_stack(), exc_info=True)
        else:
            debug("%s sent. id->%s", entry.name, result.id)

    def apply_async(
        self,
        entry: Entry,
        producer: Optional[Producer] = None,
        advance: bool = True,
        **kwargs,
    ) -> None:
        # Update time-stamps and run counts before we actually execute,
        # so we have that done if an exception is raised (doesn't schedule
        # forever.)
        entry = self.reserve(entry) if advance else entry
        signature = entry.sig

        try:
            return signature.apply_async(producer=producer)
        except Exception as exc:  # pylint: disable=broad-except
            reraise(
                SchedulingError,
                SchedulingError(
                    f"Couldn't apply scheduled signature {entry.name}: {exc}"
                ),
                sys.exc_info()[2],
            )
        finally:
            self._tasks_since_sync += 1
            if self.should_sync():
                self._do_sync()

    def send_task(self, *args, **kwargs):
        return self.app.send_task(*args, **kwargs)
