from src.base.base_schemas import BaseSchema


class EmployeeSchemaMinimal(BaseSchema):
    id: int | None
    name: str
    last_name: str | None
    middle_name: str | None
    email: str | None
    phone_number: str | None
    # organisation: OrganisationSchemaMinimal | None
    # department: DepartmentSchemaMinimal | None
    # position: PositionSchemaMinimal | None
