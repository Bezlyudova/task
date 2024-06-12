from pydantic import BaseModel


class DepartmentSchemaCreate(BaseModel):
    name: str | None
    phone_number: str | None
    organisation_id: int
    master_id:  int | None = None
