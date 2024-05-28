from fastapi_users import schemas
from src.base.base_schemas import BaseSchema
from src.features.department.schemas.department_schema_minimal import DepartmentSchemaMinimal
from src.features.organisation.schemas.organisation_schema_minimal import OrganisationSchemaMinimal
from src.features.position.schemas.position_schema_minimal import PositionSchemaMinimal


class EmployeeSchema(schemas.BaseUser[int], BaseSchema):
    id: int | None
    name: str
    last_name: str
    middle_name: str | None
    email: str
    phone_number: str | None
    organisation: OrganisationSchemaMinimal | None = None
    department: DepartmentSchemaMinimal | None = None
    position: PositionSchemaMinimal | None = None
