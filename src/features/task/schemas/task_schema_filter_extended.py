from typing import Optional, List

from src.features.task.schemas.task_schema_filter import TaskSchemaFilter
from src.task_state_enum import TaskStateEnum


class TaskSchemaFilterExtended(TaskSchemaFilter):
    assigner_id: int | None
    observer_id: int | None
    state: List[TaskStateEnum] | None
    # is_hidden: bool | None
