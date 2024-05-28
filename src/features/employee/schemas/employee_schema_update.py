from pydantic import BaseModel


class EmployeeSchemaUpdate(BaseModel):
    name: str | None
    last_name: str | None
    middle_name: str | None
    email: str | None
    phone_number: str | None
    position_id: int | None
    organisation_id: int | None
    department_id: int | None
