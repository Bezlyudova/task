from src.base.base_service import BaseService, BaseRepository
from src.features.employee.repositories.employee_repository import EmployeeRepository


class EmployeeService(BaseService):
    @property
    def repository(self) -> BaseRepository:
        return EmployeeRepository(self.req)
