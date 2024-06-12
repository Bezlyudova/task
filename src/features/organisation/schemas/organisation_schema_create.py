from pydantic import BaseModel


class OrganisationSchemaCreate(BaseModel):
    phone_number: str
    name: str
    note: str | None = None
    master_id: int | None = None
