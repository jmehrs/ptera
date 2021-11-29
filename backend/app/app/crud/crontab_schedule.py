from app.crud.crud_base import CRUDBase
from app.models.crontab_schedule import CrontabSchedule
from app.schemas.crontab_schedule import CrontabScheduleCreate, CrontabScheduleUpdate


class CRUDCrontabSchedule(
    CRUDBase[CrontabSchedule, CrontabScheduleCreate, CrontabScheduleUpdate]
):
    pass


crontab_schedule = CRUDCrontabSchedule(CrontabSchedule)
