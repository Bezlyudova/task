from pydantic import BaseModel


class TaskAndAssignerSchemaUpdate(BaseModel):
    note: str | None
