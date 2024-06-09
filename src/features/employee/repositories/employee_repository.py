from itertools import chain
from typing import Type, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, with_loader_criteria

from src.base.base_exception import BaseExceptionCustom
from src.base.base_repository import BaseRepo, ModelType, SchemaType, CreateSchemaType
from src.base.base_service import AsyncSession
from src.features.department.entities.department_entity import Department
from src.features.employee.entities.employee_entity import Employee
from src.features.employee.schemas.employee_schema import EmployeeSchema
from src.features.employee.schemas.employee_schema_create import EmployeeSchemaCreate
from src.features.employee.schemas.employee_schema_filter import EmployeeSchemaFilter
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal
from src.features.employee.schemas.employee_schema_update import EmployeeSchemaUpdate
from src.features.position.entities.position_entity import Position


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

    @property
    def common_options(self):
        return [
            *super().common_options,
            (
                joinedload(Employee.position).joinedload(Position.department).joinedload(Department.organisation),
                with_loader_criteria(Department, Department.is_deleted != True),
            ),
            (
                joinedload(Employee.department).joinedload(Department.organisation),
                with_loader_criteria(Department, Department.is_deleted != True),
            ),
        ]


    async def login(
        self, session: AsyncSession, login: str
    ) -> EmployeeSchema:
        req = select(Employee).options(*chain(*self.common_options)).where(Employee.email==login)
        res = (await session.execute(req)).scalar()
        if res is None:
            raise BaseExceptionCustom(
                status_code=404,
                reason=f"{self.model.__name__ } with current ID: < {id} > was not found",
                message=f"Объект не найден",
            )
        result = self.schema.from_orm(res)
        return result

    def add_full_name_filter_to_query_options(
        self, query, full_name: Optional[str]
    ) -> int:
        if full_name:
            query.append(
                func.to_tsvector(
                    func.concat_ws(
                        " ",
                        self.model.name,
                        self.model.middle_name,
                        self.model.last_name,
                    )
                ).bool_op("@@")(
                    func.to_tsquery(f'{":* & ".join(full_name.strip().split(" "))}:*')
                )
            )
        return query

    def get_filter_query(self, filter_schema, without_deleted):
        res = super().get_filter_query(filter_schema, without_deleted)
        return self.add_full_name_filter_to_query_options(res, filter_schema.full_name)