from typing import Type

from src.base.base_repository import BaseRepo, ModelType, SchemaType, CreateSchemaType
from src.features.organisation.entities.organisation_entity import Organisation
from src.features.organisation.schemas.organisation_schema import OrganisationSchema
from src.features.organisation.schemas.organisation_schema_create import OrganisationSchemaCreate
from src.features.organisation.schemas.organisation_schema_filter import OrganisationSchemaFilter
from src.features.organisation.schemas.organisation_schema_minimal import OrganisationSchemaMinimal
from src.features.organisation.schemas.organisation_schema_update import OrganisationSchemaUpdate


class OrganisationRepository(BaseRepo):
    @property
    def model(self) -> Type[ModelType]:
        return Organisation

    @property
    def schema(self) -> Type[SchemaType]:
        return OrganisationSchema

    @property
    def create_schema(self) -> Type[CreateSchemaType]:
        return OrganisationSchemaCreate

    @property
    def update_schema(self) -> Type[OrganisationSchemaUpdate]:
        return OrganisationSchemaUpdate

    @property
    def minimal_schema(self) -> Type[OrganisationSchemaMinimal]:
        return OrganisationSchemaMinimal

    @property
    def filter_schema(self) -> Type[OrganisationSchemaFilter]:
        return OrganisationSchemaFilter

    # @property
    # def common_options(self):
    #     return [
    #         *super().common_options,
    #         (
    #             joinedload(Employer.position).joinedload(Position.Organisation),
    #             with_loader_criteria(Position, Position.is_deleted != True),
    #         ),
    #     ]