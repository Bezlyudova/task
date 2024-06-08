from datetime import datetime
from typing import List

from src.features.task.schemas.task_schema_filter import TaskSchemaFilter
from src.task_state_enum import TaskStateEnum


class TaskSchemaFilterExtended(TaskSchemaFilter):
    assigner_id: int | None
    observer_id: int | None
    create_id: int | None
    state: List[TaskStateEnum] | None
    dead_line_date: datetime | None
    # is_hidden: bool | None
