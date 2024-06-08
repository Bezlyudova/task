import datetime
from typing import Optional, List

from src.base.base_service import BaseService, AsyncSession
from src.db.session import transactional
from src.features.task_and_assigner.repository.task_and_assigner_repository import TaskAndAssignerRepository
from src.features.task_and_assigner.schemas.complete_dump_schema_update import CompleteDumpSchemaUpdate
from src.features.task_and_assigner.schemas.task_and_assigner_dump_schema_update import TaskAndAssignerDumpSchemaUpdate
from src.features.task_and_assigner.schemas.task_and_assigner_schema import TaskAndAssignerSchema
from src.features.task_and_assigner.schemas.task_and_assigner_schema_update import TaskAndAssignerSchemaUpdate
from src.type_of_assigner import TypeOfAssigner


class TaskAndAssignerService(BaseService):
    @property
    def repository(self) -> TaskAndAssignerRepository:
        return TaskAndAssignerRepository(self.req)

    @transactional
    async def set_assigner_task_status(
        self,
        task_id: int,
        update_schema: TaskAndAssignerDumpSchemaUpdate,
        *,
        session: Optional[AsyncSession] = None,
    ):
        task_and_assigner_ids = await self.repository.get_tas_id_by_task_id(
            session=session, task_id=task_id, for_complete=False
        )
        for id in task_and_assigner_ids:
            result = await self.repository.update(
                session=session,
                id=id,
                schema_update=TaskAndAssignerSchemaUpdate.from_dump_schema(update_schema),
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
    async def complete_task_and_assigners(
        self,
        task_id: int,
        update_schema: TaskAndAssignerDumpSchemaUpdate,
        *,
        session: Optional[AsyncSession] = None,
    ) -> TaskAndAssignerSchema:
        return await self.repository.complete_task_and_assigners(
            session=session,
            id=task_id,
            schema_update=TaskAndAssignerSchemaUpdate.from_dump_schema(update_schema),
        )

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

