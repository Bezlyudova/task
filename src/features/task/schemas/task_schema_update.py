from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.task_state_enum import TaskStateEnum


class TaskSchemaUpdate(BaseModel):
    name: str | None
    description: str | None
    is_completed: bool | None
    completed_date: datetime | None
    state: TaskStateEnum | None
