from typing import Type

from sqlalchemy.orm import joinedload, with_loader_criteria

from src.base.base_repository import BaseRepo, ModelType, SchemaType, CreateSchemaType
from src.features.department.entities.department_entity import Department
from src.features.organisation.entities.organisation_entity import Organisation
from src.features.position.entities.position_entity import Position
from src.features.position.schemas.position_schema import PositionSchema
from src.features.position.schemas.position_schema_create import PositionSchemaCreate
from src.features.position.schemas.position_schema_filter import PositionSchemaFilter
from src.features.position.schemas.position_schema_minimal import PositionSchemaMinimal
from src.features.position.schemas.position_schema_update import PositionSchemaUpdate


class PositionRepository(BaseRepo):
    @property
    def model(self) -> Type[ModelType]:
        return Position

    @property
    def schema(self) -> Type[SchemaType]:
        return PositionSchema

    @property
    def create_schema(self) -> Type[CreateSchemaType]:
        return PositionSchemaCreate

    @property
    def update_schema(self) -> Type[PositionSchemaUpdate]:
        return PositionSchemaUpdate

    @property
    def minimal_schema(self) -> Type[PositionSchemaMinimal]:
        return PositionSchemaMinimal

    @property
    def filter_schema(self) -> Type[PositionSchemaFilter]:
        return PositionSchemaFilter

    @property
    def common_options(self):
        return [
            *super().common_options,
            (
                joinedload(Position.department).joinedload(Department.organisation).joinedload(Organisation.master),
                with_loader_criteria(Department, Department.is_deleted != True),
            ),
        ]