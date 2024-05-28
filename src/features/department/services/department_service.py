from src.base.base_service import BaseService, BaseRepository
from src.features.department.repositories.department_repository import DepartmentRepository


class DepartmentService(BaseService):
    @property
    def repository(self) -> BaseRepository:
        return DepartmentRepository(self.req)
