from typing import Optional

from src.base.base_service import BaseService, BaseRepository, AsyncSession
from src.db.session import transactional
from src.features.employee.repositories.employee_repository import EmployeeRepository
from src.features.employee.schemas.employee_schema import EmployeeSchema


class EmployeeService(BaseService):
    @property
    def repository(self) -> BaseRepository:
        return EmployeeRepository(self.req)

    @transactional
    async def login(
            self,
            login: int,
            *,
            session: Optional[AsyncSession] = None,
    ) -> EmployeeSchema:
        result: EmployeeSchema = await self.repository.login(session=session, login=login)
        return result