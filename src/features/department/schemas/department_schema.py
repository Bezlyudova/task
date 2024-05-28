from src.base.base_schemas import BaseSchema
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal
from src.features.organisation.schemas.organisation_schema_minimal import OrganisationSchemaMinimal
from src.features.position.schemas.position_schema_minimal import PositionSchemaMinimal


class DepartmentSchema(BaseSchema):
    name: str | None
    phone_number: str | None
    organisation_id: int
    organisation: OrganisationSchemaMinimal | None = None
    # employees: Optional[List[Optional[EmployeeSchemaMinimal]]]
    # positions: Optional[List[PositionSchemaMinimal]]
    master: EmployeeSchemaMinimal | None = None
