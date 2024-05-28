from pydantic import BaseModel


class OrganisationSchemaUpdate(BaseModel):
    phone_number: str | None
    name: str | None
    note: str | None
    master_id: int | None
