from typing import Optional, List

from src.base.base_service import BaseService, AsyncSession
from src.db.session import transactional
from src.features.task_and_assigner.repository.task_and_assigner_repository import TaskAndAssignerRepository
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
    ) -> TaskAndAssignerSchema:
        task_and_assigner_ids = await self.repository.get_tas_id_by_task_id(
            session=session, task_id=task_id, for_complete=update_schema.is_completed
        )
        for id in task_and_assigner_ids:
            result = await self.repository.update(
                session=session,
                id=id,
                schema_update=TaskAndAssignerSchemaUpdate.from_dump_schema(update_schema),
            )
        return result

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

    # @transactional
    # async def hide_all(
    #     self,
    #     task_hide_schema: TaskSchemaHide,
    #     *,
    #     session: Optional[AsyncSession] = None,
    # ) -> bool:
    #     return await self.repository.hide_all(
    #         session=session,
    #         task_ids=task_hide_schema.task_ids,
    #         schema_update=TaskAndAssignerUpdateSchema.from_dump_schema(
    #             TaskAndAssignerDumpSchemaUpdate(is_hidden=task_hide_schema.is_hidden)
    #         ),
    #     )

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

    @transactional
    async def get_all_assigners_for_tasks(
        self,
        task_id: int,
        *,
        session: Optional[AsyncSession] = None,
    ) -> List[TaskAndAssignerSchema]:
        return await self.repository.get_all_assigners_for_tasks(
            task_id=task_id, session=session
        )

    @transactional
    async def assign_started_task(
        self,
        task_id: int,
        employer_id: int,
        *,
        session: Optional[AsyncSession] = None,
    ) -> bool:
        from src.features.task.services.task_service import TaskService

        task = await TaskService(None).get_by_id_without_activity(
            id=task_id, session=session
        )

        is_founded_observer = False
        for ass in task.assigners:
            if ass.employer_id == employer_id:
                is_founded_observer = True
            if ass.type_of_assigner == TypeOfAssigner.ASSIGNER.value:
                if ass.employer_id == employer_id:
                    return False
                return False

        if not is_founded_observer:
            return False


        await self.repository.assign_started_task(
            task_id=task_id, employer_ids=[employer_id], session=session
        )
        return True
