from datetime import datetime
from pydantic import BaseModel

from src.task_state_enum import TaskStateEnum


class TaskSchemaUpdate(BaseModel):
    name: str | None
    description: str | None
    dead_line_date: datetime | None
    state: TaskStateEnum | None
