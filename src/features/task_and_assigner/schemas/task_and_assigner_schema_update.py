from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.features.task_and_assigner.schemas.task_and_assigner_dump_schema_update import TaskAndAssignerDumpSchemaUpdate


class TaskAndAssignerSchemaUpdate(BaseModel):
    is_read: Optional[bool]
    read_date: Optional[datetime]
    is_completed: Optional[bool]
    complete_date: Optional[datetime]
    is_expired: Optional[bool]
    expired_date: Optional[datetime]
    is_hidden: Optional[bool]
    hidden_date: Optional[datetime]
    note: Optional[str]
    # color_marker: Optional[str]


    @classmethod
    def from_dump_schema(cls, val: TaskAndAssignerDumpSchemaUpdate):
        vals = val.dict(exclude_unset=True)
        current_time = datetime.now()

        if vals.get("is_read"):
            vals["read_date"] = current_time
        if vals.get("is_completed"):
            vals["complete_date"] = current_time
        if vals.get("is_expired"):
            vals["expired_date"] = current_time
        if vals.get("is_hidden"):
            vals["hidden_date"] = current_time
        return cls(**vals)
