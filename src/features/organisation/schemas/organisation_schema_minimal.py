from src.base.base_schemas import BaseSchema
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal


class OrganisationSchemaMinimal(BaseSchema):
    phone_number: str
    name: str
    note: str | None
    master: EmployeeSchemaMinimal | None
