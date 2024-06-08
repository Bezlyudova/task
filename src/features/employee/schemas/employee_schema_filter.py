from pydantic import BaseModel


class EmployeeSchemaFilter(BaseModel):
    name: str | None
    last_name: str | None
    middle_name: str | None
    email: str | None
    phone_number: str | None
    organisation_id: int | None
    department_id: int | None
    full_name: str | None
    organisation_id: int | None
    department_id: int | None
    position_id: int | None

