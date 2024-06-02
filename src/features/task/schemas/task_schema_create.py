from datetime import datetime
from pydantic import BaseModel

from src.task_state_enum import TaskStateEnum


class TaskSchemaCreate(BaseModel):
    name: str
    dead_line_date: datetime
    # is_priority: bool
    description: str | None
    state: TaskStateEnum | None
    create_id: int | None
    # warning_note: Optional[str]
