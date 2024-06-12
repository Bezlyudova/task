from datetime import datetime
from typing import List

from src.base.base_schemas import BaseSchema
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal
from src.features.task_and_assigner.schemas.task_and_assigner_schema import TaskAndAssignerSchema
from src.task_state_enum import TaskStateEnum


class TaskSchema(BaseSchema):
    name: str | None
    description: str | None

    dead_line_date: datetime | None

    is_expired: bool
    expired_date: datetime | None = None

    started_by: int | None = None
    started: EmployeeSchemaMinimal | None = None
    start_date: datetime | None = None

    is_completed: bool
    completed_date: datetime | None = None

    assigners: List[TaskAndAssignerSchema] | None = None

    state: TaskStateEnum

    priority: int | None
