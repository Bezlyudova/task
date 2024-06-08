from fastapi_users import schemas

from pydantic import BaseModel


class EmployeeSchemaCreate(schemas.BaseUserCreate, BaseModel):
    name: str
    last_name: str
    middle_name: str | None
    email: str
    phone_number: str
    organisation_id: int | None
    department_id: int | None
    position_id: int | None

    def __hash__(self):
        return hash(str(self))