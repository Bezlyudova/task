from datetime import datetime
from typing import Optional, List

from src.base.base_schemas import BaseSchema
from src.features.task_and_assigner.schemas.task_and_assigner_schema import TaskAndAssignerSchema
from src.task_state_enum import TaskStateEnum


class TaskSchema(BaseSchema):
    name: str | None
    description: str | None

    # warning_note: Optional[str]
    # is_priority: bool

    dead_line_date: datetime | None
    # new_dead_line_date: Optional[datetime]

    is_expired: bool
    # expired_date: Optional[datetime]

    # started_by: Optional[int]
    # start_date: Optional[datetime]



    is_completed: bool
    # completed_date: Optional[datetime]

    assigners: List[TaskAndAssignerSchema] | None = None

    state: TaskStateEnum
