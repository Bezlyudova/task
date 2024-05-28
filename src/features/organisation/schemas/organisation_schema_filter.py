from typing import Optional

from pydantic import BaseModel


class OrganisationSchemaFilter(BaseModel):
    phone_number: Optional[str]
    name: Optional[str]
    note: Optional[str]
