from src.base.base_schemas import BaseSchema
from src.features.department.schemas.department_schema_minimal import DepartmentSchemaMinimal
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal


class OrganisationSchema(BaseSchema):
    phone_number: str
    name: str
    note: str | None
    # departments: Optional[List[DepartmentSchemaMinimal]]
    master: EmployeeSchemaMinimal | None = None
