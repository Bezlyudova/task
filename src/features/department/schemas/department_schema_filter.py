from pydantic import BaseModel


class DepartmentSchemaFilter(BaseModel):
    name: str | None
    phone_number: str | None
    organisation_id: int | None
