from pydantic.main import BaseModel


class TaskAndAssignerDumpSchemaUpdate(BaseModel):
    is_read: bool | None
    is_completed: bool | None
    is_expired: bool | None
    note: str | None
