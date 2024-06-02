from pydantic import BaseModel


class OrganisationSchemaFilter(BaseModel):
    phone_number: str | None
    name: str | None
    note: str | None
