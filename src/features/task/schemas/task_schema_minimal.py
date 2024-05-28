from datetime import datetime
from typing import Optional, List

from src.base.base_schemas import BaseSchema
from src.features.task_and_assigner.schemas.task_and_assigner_schema_minimal import TaskAndAssignerSchemaMinimal
from src.task_state_enum import TaskStateEnum


class TaskSchemaMinimal(BaseSchema):
    name: str
    description: str | None
    # is_priority: bool | None
    dead_line_date: datetime
    is_completed: bool
    is_canceled: bool
    state: TaskStateEnum
    assigners: List[TaskAndAssignerSchemaMinimal] | None
