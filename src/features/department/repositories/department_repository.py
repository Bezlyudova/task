from typing import Type

from sqlalchemy.orm import joinedload

from src.base.base_repository import BaseRepo, ModelType, SchemaType, CreateSchemaType
from src.features.department.entities.department_entity import Department
from src.features.department.schemas.department_schema import DepartmentSchema
from src.features.department.schemas.department_schema_create import DepartmentSchemaCreate
from src.features.department.schemas.department_schema_filter import DepartmentSchemaFilter
from src.features.department.schemas.department_schema_minimal import DepartmentSchemaMinimal
from src.features.department.schemas.department_schema_update import DepartmentSchemaUpdate


class DepartmentRepository(BaseRepo):
    @property
    def model(self) -> Type[ModelType]:
        return Department

    @property
    def schema(self) -> Type[SchemaType]:
        return DepartmentSchema

    @property
    def create_schema(self) -> Type[CreateSchemaType]:
        return DepartmentSchemaCreate

    @property
    def update_schema(self) -> Type[DepartmentSchemaUpdate]:
        return DepartmentSchemaUpdate

    @property
    def minimal_schema(self) -> Type[DepartmentSchemaMinimal]:
        return DepartmentSchemaMinimal

    @property
    def filter_schema(self) -> Type[DepartmentSchemaFilter]:
        return DepartmentSchemaFilter

    # @property
    # def common_options(self):
    #     return [
    #         *super().common_options,
    #         (
    #             joinedload(Department.master),
    #         ),
    #     ]
