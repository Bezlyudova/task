from pydantic.main import BaseModel


class TaskAndAssignerDumpSchemaUpdate(BaseModel):
    is_read: bool | None
    is_expired: bool | None
