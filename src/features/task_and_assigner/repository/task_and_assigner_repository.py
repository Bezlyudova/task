from typing import Type, List

from sqlalchemy import select, delete, update

from src.base.base_repository import BaseRepo, ModelType, SchemaType
from src.base.base_service import AsyncSession
from src.features.task.entities import Task
from src.features.task_and_assigner.entities import TaskAndAssigner
from src.features.task_and_assigner.schemas.task_and_assigner_schema import TaskAndAssignerSchema
from src.features.task_and_assigner.schemas.task_and_assigner_schema_create import TaskAndAssignerSchemaCreate
from src.features.task_and_assigner.schemas.task_and_assigner_schema_filter import TaskAndAssignerSchemaFilter
from src.features.task_and_assigner.schemas.task_and_assigner_schema_minimal import TaskAndAssignerSchemaMinimal
from src.features.task_and_assigner.schemas.task_and_assigner_schema_update import TaskAndAssignerSchemaUpdate
from src.type_of_assigner import TypeOfAssigner


class TaskAndAssignerRepository(BaseRepo):
    @property
    def model(self) -> Type[ModelType]:
        return TaskAndAssigner

    @property
    def schema(self) -> Type[SchemaType]:
        return TaskAndAssignerSchema

    @property
    def update_schema(self) -> Type[TaskAndAssignerSchemaUpdate]:
        return TaskAndAssignerSchemaUpdate

    @property
    def create_schema(self) -> Type[TaskAndAssignerSchemaCreate]:
        return TaskAndAssignerSchemaCreate

    @property
    def minimal_schema(self) -> Type[TaskAndAssignerSchemaMinimal]:
        return TaskAndAssignerSchemaMinimal

    @property
    def filter_schema(self) -> Type[TaskAndAssignerSchemaFilter]:
        return TaskAndAssignerSchemaFilter

    async def get_tas_id_by_task_id(
        self,
        session: AsyncSession,
        task_id: int,
        for_complete: bool,
    ) -> List[int]:
        """
        Метод для получения TaskAndAssigner.id по Task.id для авторизованного пользователя
        :param session: sqlalchemy session abstraction
        :param task_id: id Task
        :param for_complete: задача БУДЕТ помечена как завершенная?
        :return: List[id] TaskAndAssigner (assigner+observer)
        """
        query = (
            select(TaskAndAssigner.id).where(
                TaskAndAssigner.employee_id == 1
            )
        ).where(TaskAndAssigner.task_id == task_id)
        if for_complete:
            query = query.where(
                Task.is_deleted != True,
                TaskAndAssigner.is_deleted != True,
            )
        task_and_assigner_ids = (await session.execute(query)).scalars()
        return task_and_assigner_ids

    async def complete_task_and_assigners(
        self, session: AsyncSession, id: int, schema_update: TaskAndAssignerSchemaUpdate
    ) -> TaskAndAssignerSchema:
        await session.execute(
            update(TaskAndAssigner)
            .where(TaskAndAssigner.task_id == id)
            .values(schema_update.dict(exclude_unset=True))
        )
        return await self.get_by_id_without_activity(session, id)

    async def get_completed(
        self,
        session: AsyncSession,
        task_id: int,
    ) -> List[bool]:
        """
        Метод для получения статуса is_completed для всех ассигнеров по Task.id
        :param session: sqlalchemy session abstraction
        :param task_id: id Task
        :return: лист bool
        """
        completed = (
            (
                await session.execute(
                    select(TaskAndAssigner.is_completed)
                    .where(
                        TaskAndAssigner.task_id == task_id,
                        TaskAndAssigner.is_deleted != True,
                        Task.is_deleted != True,
                        TaskAndAssigner.type_of_assigner == TypeOfAssigner.ASSIGNER,
                    )
                    .where(TaskAndAssigner.task_id == Task.id)
                )
            )
            .scalars()
            .all()
        )

        return completed

    async def delete_all_assigners_for_task(
        self, task_id: int, type_of_assigner: TypeOfAssigner, session: AsyncSession
    ):
        await session.execute(
            delete(TaskAndAssigner).where(
                TaskAndAssigner.task_id == task_id,
                TaskAndAssigner.type_of_assigner == type_of_assigner.name,
            )
        )
