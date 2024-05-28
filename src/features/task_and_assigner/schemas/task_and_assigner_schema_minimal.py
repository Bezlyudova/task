from typing import Optional

from src.base.base_schemas import BaseSchema
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal
from src.type_of_assigner import TypeOfAssigner


class TaskAndAssignerSchemaMinimal(BaseSchema):
    id: int
    task_id: int
    employee: Optional[EmployeeSchemaMinimal]
    type_of_assigner: Optional[TypeOfAssigner]
    is_read: Optional[bool]
    is_hidden: Optional[bool]
    # color_marker: Optional[str]
