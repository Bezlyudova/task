from typing import Optional, List

from src.base.base_service import BaseService, AsyncSession
from src.db.session import transactional
from src.features.task_and_assigner.repository.task_and_assigner_repository import TaskAndAssignerRepository
from src.features.task_and_assigner.schemas.complete_dump_schema_update import CompleteDumpSchemaUpdate
from src.features.task_and_assigner.schemas.read_dump_schema_update import ReadDumpSchemaUpdate
from src.type_of_assigner import TypeOfAssigner


class TaskAndAssignerService(BaseService):
    @property
    def repository(self) -> TaskAndAssignerRepository:
        return TaskAndAssignerRepository(self.req)

    @transactional
    async def read_assigner_task_status(
        self,
        task_id: int,
        update_schema: ReadDumpSchemaUpdate,
        *,
        session: Optional[AsyncSession] = None,
    ):
        await self.repository.read_task_for_assigner(
            session=session,
            id=task_id,
            update_schema=update_schema,
        )
        return True

    @transactional
    async def complete_task_for_assigner(
        self,
        task_id: int,
        update_schema: CompleteDumpSchemaUpdate,
        *,
        session: Optional[AsyncSession] = None,
    ):
        await self.repository.complete_task_for_assigner(
            session=session,
            id=task_id,
            update_schema=update_schema,
        )
        return True

    @transactional
    async def get_completed(
        self,
        task_id: int,
        *,
        session: Optional[AsyncSession] = None,
    ) -> List[bool]:
        return await self.repository.get_completed(session=session, task_id=task_id)

    @transactional
    async def delete_all_assigners_for_task(
        self,
        task_id: int,
        type_of_assigner: TypeOfAssigner,
        *,
        session: Optional[AsyncSession] = None,
    ):
        return await self.repository.delete_all_assigners_for_task(
            task_id=task_id, type_of_assigner=type_of_assigner, session=session
        )

