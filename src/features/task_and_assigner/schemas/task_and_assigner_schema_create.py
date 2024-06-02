from pydantic import BaseModel
from src.type_of_assigner import TypeOfAssigner


class TaskAndAssignerSchemaCreate(BaseModel):
    task_id: int
    employee_id: int
    type_of_assigner: TypeOfAssigner
    # note: Optional[str]
