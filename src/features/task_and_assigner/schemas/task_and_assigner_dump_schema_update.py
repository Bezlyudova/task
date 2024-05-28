from typing import Optional

from pydantic.main import BaseModel

class TaskAndAssignerDumpSchemaUpdate(BaseModel):
    is_read: Optional[bool]
    is_completed: Optional[bool]
    is_expired: Optional[bool]
    is_hidden: Optional[bool]
    note: Optional[str]
