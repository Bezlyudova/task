from src.base.base_schemas import BaseSchema
from src.features.organisation.schemas.organisation_schema_minimal import OrganisationSchemaMinimal


class DepartmentSchemaMinimal(BaseSchema):
    name: str
    phone_number: str
    organisation: OrganisationSchemaMinimal
