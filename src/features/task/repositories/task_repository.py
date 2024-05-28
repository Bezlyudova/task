from itertools import chain
from typing import Type, List

from sqlalchemy import select, func, distinct, or_, and_
from sqlalchemy.orm import joinedload

from src.base.base_exception import BaseExceptionCustom
from src.base.base_repository import BaseRepo, ModelType, CreateSchemaType, MinimalSchemaType
from src.base.base_schemas import SchemaType, BasePaginationSchema
from src.base.base_service import AsyncSession
from src.features.task.entities import Task
from src.features.task.schemas.task_schema import TaskSchema
from src.features.task.schemas.task_schema_create import TaskSchemaCreate
from src.features.task.schemas.task_schema_filter import TaskSchemaFilter
from src.features.task.schemas.task_schema_filter_extended import TaskSchemaFilterExtended
from src.features.task.schemas.task_schema_minimal import TaskSchemaMinimal
from src.features.task.schemas.task_schema_update import TaskSchemaUpdate
from src.features.task_and_assigner.entities import TaskAndAssigner
from src.type_of_assigner import TypeOfAssigner


class TaskRepository(BaseRepo):
    @property
    def model(self) -> Type[ModelType]:
        return Task

    @property
    def schema(self) -> Type[SchemaType]:
        return TaskSchema

    @property
    def create_schema(self) -> Type[CreateSchemaType]:
        return TaskSchemaCreate

    @property
    def update_schema(self) -> Type[TaskSchemaUpdate]:
        return TaskSchemaUpdate

    @property
    def minimal_schema(self) -> Type[MinimalSchemaType]:
        return TaskSchemaMinimal

    @property
    def filter_schema(self) -> Type[TaskSchemaFilter]:
        return TaskSchemaFilter

    @property
    def common_options(self):
        return [
            *super().common_options,
            # (joinedload(Task.creator),),
            (
                joinedload(Task.assigners).joinedload(TaskAndAssigner.employee),
                # with_loader_criteria(employee, employee.is_deleted != True),
            ),
            # (
            #     joinedload(Task.creator).joinedload(employee.position),
            #     with_loader_criteria(
            #         employeeOrganisation, employeeOrganisation.is_deleted != True
            #     ),
            # ),
            # (
            #     joinedload(Task.creator).joinedload(employee.department),
            #     with_loader_criteria(Department, Department.is_deleted != True),
            # ),
            # (
            #     joinedload(Task.creator).joinedload(employee.organisation),
            #     with_loader_criteria(
            #         employeeOrganisation, employeeOrganisation.is_deleted != True
            #     ),
            # ),
            # (
            #     joinedload(Task.children)
            #     .joinedload(Task.assigners)
            #     .joinedload(TaskAndAssigner.employee),
            # ),
        ]


    async def get_by_id(
        self, user, session: AsyncSession, id: int, without_deleted=True
    ) -> SchemaType:
        return await self.get_by_id_without_activity(user=user, session=session, id=id, without_deleted=without_deleted)


    async def get_by_id_without_activity(
        self, user, session: AsyncSession, id: int, without_deleted=False
    ) -> SchemaType:
        """
        :param session: sqlalchemy session abstraction
        :param id: id записи
        :param without_deleted: По умолчанию - True выбираем только записи не помеченные как удаленные
        :return: Запись или None
        """
        req = select(self.model).options(*chain(*self.common_options))
        where_options = [self.model.id == id]
        if without_deleted:
            where_options.append(self.model.is_deleted != True)

        res = (await session.execute(req.where(*where_options))).scalar()
        if res is None:
            raise BaseExceptionCustom(
                status_code=404,
                reason=f"{self.model.__name__ } with current ID: < {id} > was not found",
                message=f"Объект не найден",
            )
        result = self.schema.from_orm(res)
        return result

    async def get_count_unreaded_task(
        self,
        user,
        session: AsyncSession,
    ):
        query_count = session.execute(
            select((func.count(distinct(Task.id))))
            # .where(Task.state != TaskStateEnum.DRAFT)
            # .where(Task.state != TaskStateEnum.COMPLETED)
            # .where(Task.state != TaskStateEnum.TERMINATED)
            .where(TaskAndAssigner.employee_id == user.id)
            .join(TaskAndAssigner, TaskAndAssigner.task_id == Task.id)
            .where(TaskAndAssigner.is_read == False)
            .where(
                or_(
                    TaskAndAssigner.type_of_assigner == "ASSIGNER",
                    TaskAndAssigner.type_of_assigner == "OBSERVER"
                )
            )
        )
        return (await query_count).scalar()

    # async def get_by_id(
    #     self, session: AsyncSession, id: int, without_deleted=True
    # ) -> SchemaType:
    #     await check_permissions(
    #         session, self.request.user.id, TypeOfEntity.TASK, id, ActivityType.READ
    #     )
    #     return await self.get_by_id_without_activity(session, id, without_deleted)

    # async def get_count_assigned(
    #     self, session: AsyncSession, type_of_assigner: str
    # ) -> int:
    #     res = (
    #         await session.execute(
    #             text(
    #                 f"select count(*) from task INNER JOIN task_and_assigner ON task_and_assigner.task_id = task.id "
    #                 f"WHERE task_and_assigner.employee_id = {self.request.user.id}"
    #                 f" and task_and_assigner.type_of_assigner = '{type_of_assigner}'"
    #                 f"and task.state != 'DRAFT'"
    #                 f"and task.state != 'COMPLETED'"
    #                 f"and task.state != 'TERMINATED'"
    #             )
    #         )
    #     ).scalar()
    # 
    #     return res or 0
    # 
    # @activity_log(ActivityType.UPDATE)
    # async def start_task(
    #     self, session: AsyncSession, task_id: int, new_dead_line: DateTime
    # ):
    #     task: TaskSchema = await self.get_by_id_without_activity(session, task_id)
    #     if (
    #         task.state != TaskStateEnum.DRAFT.name
    #         and task.state != TaskStateEnum.STOPPED.name
    #         and task.state != TaskStateEnum.IN_ACCEPTANCE.name
    #     ):
    #         raise TaskStateException(
    #             status_code=400,
    #             reason=f"Cant complete task with state [<{task.state}>]. Only [DRAFT/STOPPED/IN_ACCEPTANCE] state available.",
    #             message="Задача не может быть отправлена, т.к. имеет статус отличный от 'Черновик', 'Остановлена', 'На приемке'",
    #         )
    #     await session.execute(
    #         update(self.model)
    #         .where(self.model.id == task_id)
    #         .values(
    #             state=TaskStateEnum.WORKS.name,
    #             start_date=datetime.datetime.now(),
    #             new_dead_line_date=new_dead_line if new_dead_line else None,
    #         )
    #     )
    #     await session.flush()
    #     return task
    # 
    # @activity_log(ActivityType.UPDATE)
    # async def stop_task(self, session: AsyncSession, task_id: int):
    #     task: TaskSchema = await self.get_by_id_without_activity(session, task_id)
    #     if task.state != TaskStateEnum.WORKS.name:
    #         raise TaskStateException(
    #             status_code=400,
    #             reason=f"Cant complete task with state [<{task.state}>]. Only [WORKS] state available.",
    #             message="Задача не может быть остановлена, т.к. имеет статус отличный от 'В работе'",
    #         )
    #     await session.execute(
    #         update(self.model)
    #         .where(self.model.id == task_id)
    #         .values(
    #             state=TaskStateEnum.STOPPED,
    #             canceled_by_id=self.request.user.id,
    #             is_canceled=True,
    #         )
    #     )
    #     await session.flush()
    # 
    #     return task
    # 
    # @activity_log(ActivityType.UPDATE)
    # async def complete_task(self, session: AsyncSession, task_id: int):
    #     task: TaskSchema = await self.get_by_id_without_activity(session, task_id)
    #     if task.state != TaskStateEnum.WORKS.name:
    #         raise TaskStateException(
    #             status_code=400,
    #             reason=f"Cant complete task with state [<{task.state}>]. Only [WORKS] state available.",
    #             message="Задача не может быть завершена, т.к. имеет статус отличный от 'В работе'",
    #         )
    #     await session.execute(
    #         update(self.model)
    #         .where(self.model.id == task_id)
    #         .values(
    #             state=TaskStateEnum.COMPLETED,
    #             completed_date=datetime.datetime.now(),
    #             is_completed=True,
    #         )
    #     )
    #     await session.flush()
    # 
    #     return task

    async def get_with_filter(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        filtered_schema: TaskSchemaFilterExtended,
        without_deleted=True,
    ) -> BasePaginationSchema[MinimalSchemaType]:
        query_filter = self.get_filter_query(
            filter_schema=filtered_schema, without_deleted=without_deleted
        )

        count_query = select(func.count(distinct(Task.id))).where(*query_filter)

        data_query = select(distinct(Task.id)).where(*query_filter)

        count_query = self.add_assigner_filter(
            data_query=count_query,
            assign_id=filtered_schema.assigner_id,
            observer_id=filtered_schema.observer_id
        )

        data_query = self.add_assigner_filter(
            data_query=data_query,
            assign_id=filtered_schema.assigner_id,
            observer_id=filtered_schema.observer_id
        )

        count = (await session.execute(count_query)).scalar()

        data = await self.get_all_tasks_by_ids(
            ids=(
                await session.execute(
                    data_query.limit(limit).offset((offset - 1) * limit)
                )
            )
            .scalars()
            .all(),
            session=session,
        )

        data = BasePaginationSchema[self.minimal_schema](
            total=count, data=data, limit=limit, offset=offset
        )
        return data

    def add_assigner_filter(
        self,
        data_query,
        assign_id: int,
        observer_id: int,
    ):
        if observer_id or assign_id:
            data_query = data_query.join(
                TaskAndAssigner, TaskAndAssigner.task_id == Task.id
            ).where(
                or_(
                    and_(
                        *self._get_where_assigner_query(
                            assign_id=assign_id,
                            type_of_assigner=TypeOfAssigner.ASSIGNER,
                        )
                    ),
                    and_(
                        *self._get_where_assigner_query(
                            assign_id=observer_id,
                            type_of_assigner=TypeOfAssigner.OBSERVER,
                        )
                    ),
                )
            )
        return data_query

    def _get_where_assigner_query(
        self,
        assign_id: int,
        type_of_assigner: TypeOfAssigner,
    ):
        query = [
            TaskAndAssigner.employee_id.in_([assign_id]),
            TaskAndAssigner.type_of_assigner == type_of_assigner.value,
        ]

        return query

    async def get_all_tasks_by_ids(
        self, ids: List[int], session: AsyncSession
    ) -> List[TaskSchema]:
        data = await session.execute(
            select(Task).options(*chain(*self.common_options)).where(Task.id.in_(ids))
        )
        return self.transform_many_minimal(data.scalars().unique())
    #
    # async def check_expired(self, session: AsyncSession):
    #     await session.execute(
    #         update(TaskAndAssigner)
    #         .where(
    #             TaskAndAssigner.task_id.in_(
    #                 select(Task.id).where(
    #                     or_(
    #                         and_(
    #                             Task.new_dead_line_date != None,
    #                             (
    #                                 Task.new_dead_line_date
    #                                 < datetime.datetime.now().astimezone()
    #                             ),
    #                         ),
    #                         and_(
    #                             Task.new_dead_line_date == None,
    #                             (
    #                                 Task.first_dead_line_date
    #                                 < datetime.datetime.now().astimezone()
    #                             ),
    #                         ),
    #                     ),
    #                     TaskAndAssigner.is_expired != True,
    #                     Task.is_deleted != True,
    #                     Task.is_completed != True,
    #                     Task.is_canceled != True,
    #                     TaskAndAssigner.is_deleted != True,
    #                     TaskAndAssigner.is_completed != True,
    #                 )
    #             ),
    #         )
    #         .values(is_expired=True, expired_date=datetime.datetime.now())
    #     )

    # async def check_not_expired(self, session: AsyncSession):
    #     await session.execute(
    #         update(TaskAndAssigner)
    #         .where(
    #             TaskAndAssigner.task_id.in_(
    #                 select(Task.id).where(
    #                     or_(
    #                         and_(
    #                             Task.new_dead_line_date != None,
    #                             (
    #                                 Task.new_dead_line_date
    #                                 > datetime.datetime.now().astimezone()
    #                             ),
    #                         ),
    #                         and_(
    #                             Task.new_dead_line_date == None,
    #                             (
    #                                 Task.first_dead_line_date
    #                                 > datetime.datetime.now().astimezone()
    #                             ),
    #                         ),
    #                     ),
    #                     TaskAndAssigner.is_expired != False,
    #                     Task.is_deleted != True,
    #                     Task.is_completed != True,
    #                     Task.is_canceled != True,
    #                     TaskAndAssigner.is_deleted != True,
    #                     TaskAndAssigner.is_completed != True,
    #                 )
    #             )
    #         )
    #         .values(is_expired=False)
    #     )
