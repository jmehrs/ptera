from app.crud.crud_base import CRUDBase
from app.models.interval_schedule import IntervalSchedule
from app.schemas.interval_schedule import IntervalScheduleCreate, IntervalScheduleUpdate


class CRUDIntervalSchedule(
    CRUDBase[IntervalSchedule, IntervalScheduleCreate, IntervalScheduleUpdate]
):
    pass


interval_schedule = CRUDIntervalSchedule(IntervalSchedule)
