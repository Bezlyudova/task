from pydantic.main import BaseModel


class TaskAndAssignerSchemaFilter(BaseModel):
    task_id: int | None
    employer_id: int | None
