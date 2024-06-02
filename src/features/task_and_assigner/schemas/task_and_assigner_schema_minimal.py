from src.base.base_schemas import BaseSchema
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal
from src.type_of_assigner import TypeOfAssigner


class TaskAndAssignerSchemaMinimal(BaseSchema):
    id: int
    task_id: int
    employee: EmployeeSchemaMinimal | None
    type_of_assigner: TypeOfAssigner | None
    is_read: bool | None
