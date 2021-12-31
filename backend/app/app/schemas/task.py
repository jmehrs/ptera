from __future__ import annotations

from celery import Task, signature
from typing import Optional, List, Dict
from celery.canvas import Signature
from pydantic import BaseModel, Field, root_validator
from json import dumps
from app.core.celery_app import celery_tasks
from app.utils.utils import get_all_occurences


class TaskBaseModel(BaseModel):
    """BaseModel subclass that contains all task-specific functionality"""

    @classmethod
    def from_task(cls, task: Task):
        args = {field: getattr(task, field, None) for field in cls.__fields__}
        return cls(**args)


class TaskConfig(TaskBaseModel):
    """Data scheme of a celery task configuration"""

    max_retries: int = Field(
        3,
        title="The maximum number of attempted retries before giving up",
        ge=0,
    )
    default_retry_delay: Optional[int]
    rate_limit: Optional[str]
    retry_backoff: Optional[bool]
    retry_backoff_max: Optional[int]
    retry_jitter: Optional[bool]
    ignore_result: Optional[bool]
    store_errors_even_if_ignored: Optional[bool]
    serializer: Optional[str]
    soft_time_limit: Optional[int]
    time_limit: Optional[int]
    track_started: Optional[bool]
    acks_late: Optional[bool]
    acks_on_failure_or_timeout: Optional[bool]
    reject_on_worker_lost: Optional[bool]
    store_eager_result: Optional[bool]
    priority: Optional[int]


class TaskSignature(TaskBaseModel):
    """Data scheme of a celery task signature"""

    task: str
    args: Optional[List] = Field(default_factory=list)
    kwargs: Optional[Dict] = Field(default_factory=dict)
    options: Optional[Dict] = Field(default_factory=dict)
    subtask_type: Optional[str] = None
    immutable: bool = False

    @root_validator
    def validate_tasks(cls, values: Dict) -> None:
        tasks = set(get_all_occurences("task", values))
        if invalid_tasks := tasks - celery_tasks():
            raise ValueError(f"Invalid tasks were specified: {invalid_tasks}")
        return values

    @classmethod
    def from_signature(cls, sig: Signature) -> TaskSignature:
        return cls(**sig)

    def to_signature(self) -> Signature:
        return signature(self.dict())

    def to_json(self) -> str:
        signature = self.to_signature()
        return dumps(signature)


class TaskID(BaseModel):
    """Data scheme of a celery task result"""

    id: str
