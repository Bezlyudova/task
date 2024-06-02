from src.base.base_schemas import BaseSchema
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal
from src.type_of_assigner import TypeOfAssigner


class TaskAndAssignerSchema(BaseSchema):
    id: int

    task_id: int
    #
    # note: Optional[str]
    #
    employee_id: int
    employee: EmployeeSchemaMinimal | None = None

    type_of_assigner: TypeOfAssigner | None

    is_read: bool | None
    # read_date: Optional[datetime]
    #
    is_completed: bool | None
    # complete_date: Optional[datetime]
    #
    is_expired: bool | None
    # expired_date: Optional[datetime]
    #
    #
    # color_marker: Optional[str]
