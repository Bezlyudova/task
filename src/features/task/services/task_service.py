from typing import Optional, List

from src.base.base_exception import BaseExceptionCustom
from src.base.base_repository import MinimalSchemaType
from src.base.base_schemas import BasePaginationSchema
from src.base.base_service import BaseService, BaseRepository, AsyncSession
from src.db.session import transactional
from src.entity_type import TypeOfEntity
from src.features.department.services.department_service import DepartmentService
from src.features.employee.services.employee_service import EmployeeService
from src.features.task.schemas.task_schema import TaskSchema
from src.features.task.schemas.task_schema_create import TaskSchemaCreate
from src.features.task.schemas.task_schema_create_assigner import TaskSchemaCreateAssigner
from src.features.task.schemas.task_schema_filter import TaskSchemaFilter
from src.features.task.schemas.task_schema_minimal import TaskSchemaMinimal
from src.features.task.schemas.task_schema_update import TaskSchemaUpdate
from src.features.task.schemas.task_schema_update_assigners import TaskSchemaUpdateAssigner
from src.features.task.schemas.type_of_assigner_schema import TypeOfAssignerSchema
from src.features.task_and_assigner.schemas.task_and_assigner_dump_schema_update import TaskAndAssignerDumpSchemaUpdate
from src.features.task_and_assigner.schemas.task_and_assigner_schema import TaskAndAssignerSchema
from src.features.task_and_assigner.schemas.task_and_assigner_schema_create import TaskAndAssignerSchemaCreate
from src.features.task_and_assigner.services.task_and_assigner_service import TaskAndAssignerService
from src.task_state_enum import TaskStateEnum
from src.type_of_assigner import TypeOfAssigner


class TaskService(BaseService):
    @property
    def repository(self) -> BaseRepository:
        from src.features.task.repositories.task_repository import TaskRepository

        return TaskRepository(self.req)

    @property
    def department_service(self) -> DepartmentService:
        return DepartmentService(req=self.req, session=self.async_session)

    @property
    def employee_service(self) -> EmployeeService:
        return EmployeeService(req=self.req, session=self.async_session)

    @property
    def task_and_assigner_service(self) -> TaskAndAssignerService:
        return TaskAndAssignerService(req=self.req, session=self.async_session)


    @transactional
    async def get_by_id(
            self,
            id: int,
            *,
            session: Optional[AsyncSession] = None,
    ) -> TaskSchema:
        result: TaskSchema = await self.repository.get_by_id(session=session, id=id)
        return result

    async def get_employee_ids_from_list_of_type_of_assigners(
        self, list_of_ass: List[TypeOfAssignerSchema], session: AsyncSession
    ):
        ids_list: List[int] = list()

        for assigner in list_of_ass:
            if assigner.entity_type is TypeOfEntity.EMPLOYEE:
                ids_list.append(
                    (
                        await self.employee_service.get_by_id_without_activity(
                            id=assigner.entity_id, session=session
                        )
                    ).id
                )
            else:
                raise BaseExceptionCustom(
                    status_code=400,
                    reason=f"{assigner.entity_type} is not available for TaskCreation!",
                    message=f"Неверный тип сущности указан как получатель задачи",
                )
        return list(set(ids_list))

    async def _assigners_transform(
        self, schema_create: TaskSchemaCreateAssigner, session: AsyncSession
    ) -> TaskSchemaCreateAssigner:
        # Трансформирую энтитию входящую в энтитю для создания тасков, потому что оно не хочет жрать
        # поля assigners и observers

        schema_create.assigners = (
            await self.get_employee_ids_from_list_of_type_of_assigners(
                list_of_ass=schema_create.assigners,
                session=session if schema_create.assigners else [],
            )
        )
        schema_create.observers = (
            await self.get_employee_ids_from_list_of_type_of_assigners(
                list_of_ass=schema_create.observers,
                session=session if schema_create.observers else [],
            )
        )
        return schema_create


    async def _create(
        self,
        schema_create: TaskSchemaCreateAssigner,
        *,
        session: Optional[AsyncSession] = None,
        is_system: bool,
    ):
        task_schema_create: TaskSchemaCreate = TaskSchemaCreate(**dict(schema_create))
        task_schema_create.create_id = 1

        schema_create = await self._assigners_transform(
            schema_create=schema_create, session=session
        )

        new_task = await self.repository.create(
            session=session,
            schema_create=task_schema_create,
        )
        await self.add_assigners(
            employees_ids=schema_create.assigners,
            task_id=new_task.id,
            type_of_assigner=TypeOfAssigner.ASSIGNER,
            session=session,
        )

        await self.add_assigners(
            employees_ids=schema_create.observers,
            task_id=new_task.id,
            type_of_assigner=TypeOfAssigner.OBSERVER,
            session=session,
        )

        result = await self.repository.get_by_id_without_activity(
            session=session, id=new_task.id
        )
        return result

    @transactional
    async def create(
        self,
        schema_create: TaskSchemaCreateAssigner,
        # schema_create: TaskSchemaCreate,
        *,
        session: Optional[AsyncSession] = None,
    ) -> TaskSchema:
        return await self._create(
            schema_create=schema_create, session=session, is_system=False
        )

    # @transactional
    # async def create_system(
    #     self,
    #     schema_create: TaskSchemaCreateAssigner,
    #     *,
    #     session: Optional[AsyncSession] = None,
    # ) -> TaskSchema:
    #     return await self._create(
    #         schema_create=schema_create, session=session, is_system=True
    #     )

    @transactional
    async def update(
        self,
        id: int,
        schema_update: TaskSchemaUpdateAssigner,
        *,
        session: Optional[AsyncSession] = None,
    ) -> TaskSchema:
        task = await self.repository.get_by_id_without_activity(session=session, id=id, without_deleted=False)
        if task.state != TaskStateEnum.DRAFT.name:
            raise BaseExceptionCustom(
                status_code=406,
                reason="Task state is not DRAFT",
                message="Задача не в статусе 'Черновик'",
            )
        # добавляем и чистим емплоуерс
        # assингнерс
        if schema_update.assigners:
            await self.task_and_assigner_service.delete_all_assigners_for_task(
                task_id=task.id,
                type_of_assigner=TypeOfAssigner.ASSIGNER,
                session=session,
            )
            await self.add_assigners(
                employees_ids=await self.get_employee_ids_from_list_of_type_of_assigners(
                    list_of_ass=schema_update.assigners, session=session
                ),
                task_id=task.id,
                type_of_assigner=TypeOfAssigner.ASSIGNER,
                session=session,
            )
        # obsерверс
        if schema_update.observers:
            await self.task_and_assigner_service.delete_all_assigners_for_task(
                task_id=task.id,
                type_of_assigner=TypeOfAssigner.OBSERVER,
                session=session,
            )
            await self.add_assigners(
                employees_ids=await self.get_employee_ids_from_list_of_type_of_assigners(
                    list_of_ass=schema_update.observers, session=session
                ),
                task_id=task.id,
                type_of_assigner=TypeOfAssigner.OBSERVER,
                session=session,
            )

        schema_update.assigners = None
        schema_update.observers = None

        new_schema_update = TaskSchemaUpdate(**schema_update.__dict__)
        new_schema_update.state = task.state
        # new_schema_update.is_completed = task.is_completed

        return await self.repository.update(
            session=session, id=id, schema_update=new_schema_update
        )

    @transactional
    async def add_assigners(
        self,
        employees_ids: List[int],
        task_id: int,
        type_of_assigner: TypeOfAssigner,
        session: AsyncSession,
    ):
        for emp_id in employees_ids:
            await self.task_and_assigner_service.create(
                schema_create=TaskAndAssignerSchemaCreate(
                    employee_id=emp_id,
                    task_id=task_id,
                    type_of_assigner=type_of_assigner.name,
                ),
                session=session,
            )

        return True

    @transactional
    async def soft_delete(
        self,
        id: int,
        *,
        session: Optional[AsyncSession] = None,
    ):
        task: TaskSchema = await self.get_by_id_without_activity(id=id, session=session)

        await self.task_and_assigner_service.soft_delete_all(
            ids=[assigner.id for assigner in task.assigners], session=session
        )

        return await self.repository.soft_delete(id=id, session=session)

    @transactional
    async def soft_delete_all(
        self,
        ids: List[int],
        *,
        session: Optional[AsyncSession] = None,
    ):
        for id in ids:
            await self.soft_delete(id=id, session=session)

    @transactional
    async def get_filtered_data(
        self,
        filter_schema: TaskSchemaFilter,
        without_deleted: bool = True,
        page_number: int = 1,
        page_size: int = 10,
        *,
        session: Optional[AsyncSession] = None,
    ) -> BasePaginationSchema[MinimalSchemaType]:
        return await self.repository.get_with_filter(
            session,
            page_size,
            page_number,
            filter_schema,
            without_deleted,
        )

    async def get_count_unreaded_task(
        self,
    ) -> int:
        async with self.async_session.begin() as session:
            return await self.repository.get_count_unreaded_task(session=session)

    @transactional
    async def set_assigner_task_status(
        self,
        task_id: int,
        update_schema: TaskAndAssignerDumpSchemaUpdate,
        session: AsyncSession,
    ) -> TaskSchema:
        await self.task_and_assigner_service.set_assigner_task_status(
            task_id=task_id, update_schema=update_schema, session=session
        )
        task = await self.get_by_id_without_activity(id=task_id, session=session)
        list_completed = await self.task_and_assigner_service.get_completed(
            session=session, task_id=task_id
        )
        if (
            not (False in list_completed)
            and list_completed
            and task.state == TaskStateEnum.WORKS.value
        ):
            await self.repository.complete_task(
                task_id=task_id, session=session
            )
        return await self.get_by_id_without_activity(id=task_id, session=session)


    @transactional
    async def start_task(
        self,
        task_id: int,
        session: Optional[AsyncSession] = None,
    ):
        result = await self.repository.start_task(
            task_id=task_id, session=session
        )
        return result

    @transactional
    async def complete_task_for_all(self, task_id: int, session: AsyncSession):
        return await self.repository.complete_task(session=session, task_id=task_id)

    @transactional
    async def check_deadline(self, session: AsyncSession):
        await self.repository.check_expired(session=session)

    async def get_all_task_by_ids(
        self, ids: List[int], session: AsyncSession
    ) -> List[TaskSchemaMinimal]:
        return await self.repository.get_all_tasks_by_ids(ids=ids, session=session)

    # @transactional
    # async def complete_task_with_status(
    #     self, task_id, status: TaskStateEnum, session: Optional[AsyncSession] = None
    # ):
    #     task: TaskSchema = await self.get_by_id_without_activity(
    #         id=task_id, session=session
    #     )
    #     await self.repository.update(
    #         session=session,
    #         id=task_id,
    #         schema_update=TaskSchemaUpdate(
    #             state=status,
    #             is_completed=True,
    #             completed_date=datetime.datetime.now(),
    #         ),
    #     )
    #     guids: Set[str] = set([assigner.employee.guid for assigner in task.assigners])
    #     await self.notification_service.notify(
    #         to_employees_guids=list(guids),
    #         message=f"Задача <{task.name}> завершена со статусом <{status}>",
    #         from_entity_type=TypeOfEntity.TASK,
    #         from_entity_id=task_id,
    #         task_type=task.task_type,
    #     )
    #     if task.parent_id is not None:
    #         await self.task_comment_service.create(TaskCommentSchemaCreate(
    #             main_task_id=task.parent_id,
    #             task_id=task.id,
    #             note=f"Выполнена подзадача с темой \"{task.name}\".",
    #             employee_id=self.req.user.id,
    #         ), session=session)
