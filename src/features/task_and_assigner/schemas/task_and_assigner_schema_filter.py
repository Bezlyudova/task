from typing import Optional

from pydantic.main import BaseModel


class TaskAndAssignerSchemaFilter(BaseModel):
    task_id: Optional[int]
    employer_id: Optional[int]
