from pydantic import BaseModel


class DepartmentSchemaUpdate(BaseModel):
    name: str | None
    phone_number: str | None
    organisation_id: int | None
    master_id: int | None
