from typing import Type

from src.base.base_repository import BaseRepo, ModelType, SchemaType, CreateSchemaType
from src.features.employee.entities.employee_entity import Employee
from src.features.employee.schemas.employee_schema import EmployeeSchema
from src.features.employee.schemas.employee_schema_create import EmployeeSchemaCreate
from src.features.employee.schemas.employee_schema_filter import EmployeeSchemaFilter
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal
from src.features.employee.schemas.employee_schema_update import EmployeeSchemaUpdate


class EmployeeRepository(BaseRepo):
    @property
    def model(self) -> Type[ModelType]:
        return Employee

    @property
    def schema(self) -> Type[SchemaType]:
        return EmployeeSchema

    @property
    def create_schema(self) -> Type[CreateSchemaType]:
        return EmployeeSchemaCreate

    @property
    def update_schema(self) -> Type[EmployeeSchemaUpdate]:
        return EmployeeSchemaUpdate

    @property
    def minimal_schema(self) -> Type[EmployeeSchemaMinimal]:
        return EmployeeSchemaMinimal

    @property
    def filter_schema(self) -> Type[EmployeeSchemaFilter]:
        return EmployeeSchemaFilter

    # @property
    # def common_options(self):
    #     return [
    #         *super().common_options,
    #         (
    #             joinedload(Employer.position).joinedload(Position.department),
    #             with_loader_criteria(Position, Position.is_deleted != True),
    #         ),
    #     ]