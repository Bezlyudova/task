from abc import ABC, abstractmethod
from typing import TypeVar, Annotated, Optional, List, Type
from fastapi import Request

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.base.base_repository import BaseRepo, MinimalSchemaType
from src.base.base_schemas import BasePaginationSchema
from src.db.session import get_session, transactional

AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]

BaseRepository = TypeVar("BaseRepository", bound=BaseRepo)


class BaseService(
    ABC,
):
    @property
    @abstractmethod
    def repository(self) -> BaseRepository:
        ...

    def __init__(self, session: AsyncSession, req: Request = None) -> None:
        self.async_session = session
        self.req = req

    @transactional
    async def create(
            self,
            user,
            schema_create: BaseRepo.create_schema,
            *,
            session: Optional[AsyncSession] = None,
    ):
        """
        :param schema_create: Данные необходимые для создания модели
        :param session: Опционально.  Объект сессии если не передано то создается новая сессия
        :return:
        """
        return await self.get_by_id_without_activity(
            user=user,
            id=(
                await self.repository.create(
                    user=user, session=session, schema_create=schema_create
                )
            ).id,
            session=session,
        )

    @transactional
    async def create_system(
            self,
            user,
            schema_create: BaseRepo.create_schema,
            *,
            session: Optional[AsyncSession] = None,
    ):
        """
        :param schema_create: Данные необходимые для создания модели
        :param session: Опционально.  Объект сессии если не передано то создается новая сессия
        :return:
        """
        return await self.get_by_id_without_activity(
            id=(
                await self.repository.create_system(
                    session=session, schema_create=schema_create, user=user
                )
            ).id,
            session=session,
        )

    @transactional
    async def get_by_id(
            self,
            user,
            id: int,
            *,
            session: Optional[AsyncSession] = None,
    ) -> BaseRepo.schema:
        """
        Получение данных по id
        :param id: id записи
        :param s: внешняя сессия
        :return:
        """
        return await self.repository.get_by_id(user=user, session=session, id=id)

    @transactional
    async def get_by_id_without_activity(
            self,
            user,
            id: int,
            *,
            session: Optional[AsyncSession] = None,
    ) -> BaseRepo.schema:
        """
        Получение данных по id
        :param id: id записи
        :param s: внешняя сессия
        :return:
        """
        return await self.repository.get_by_id_without_activity(user=user, id=id, session=session)

    async def get_entity_by_id(
            self,
            id: int,
            *,
            session: Optional[AsyncSession] = None,
    ) -> BaseRepo.model:
        return await self.repository.get_entity_by_id(id=id, session=session)

    @transactional
    async def update(
            self,
            user,
            id: int,
            schema_update: BaseRepo.update_schema,
            *,
            session: Optional[AsyncSession] = None,
    ) -> BaseRepo.schema:
        result = await self.repository.update(
            session=session, id=id, schema_update=schema_update, user=user
        )
        return result

    @transactional
    async def soft_delete(
            self,
            user,
            id: int,
            *,
            session: Optional[AsyncSession] = None,
    ) -> BaseRepo.schema:
        """
        Мягкое удаление
        :param id: id записи которую удаляем,
        :session: Если существует внешняя сессия
        :return:
        """
        return await self.repository.soft_delete(id=id, session=session, user=user)

    @transactional
    async def soft_delete_all(
            self,
            user,
            ids: List[int],
            *,
            session: Optional[AsyncSession] = None,
    ) -> BaseRepo.schema:
        """
        Мягкое удаление
        :param id: id записи которую удаляем,
        :session: Если существует внешняя сессия
        :return:
        """
        return await self.repository.soft_delete_all(user=user, ids=ids, session=session)

    @transactional
    async def hard_delete_all(
            self,
            ids: List[int],
            *,
            session: Optional[AsyncSession] = None,
    ) -> BaseRepo.schema:
        """
        Мягкое удаление
        :param id: id записи которую удаляем,
        :session: Если существует внешняя сессия
        :return:
        """
        return await self.repository.hard_delete_all(ids=ids, session=session)

    @transactional
    async def get_filtered_data(
            self,
            user,
            filter_schema: BaseRepo.filter_schema,
            without_deleted: bool = False,
            page_number: int = 1,
            page_size: int = 10,
            *,
            session: Optional[AsyncSession] = None,
    ) -> BasePaginationSchema[Type[MinimalSchemaType]]:
        """

        :param filter_schema:  Данные фильтра
        :param without_deleted: Без мягко удаленных записей
        :param page_number:  номер страницы (для погинации)
        :param page_size:  размер страницы(для поагинации)
        :return:
        """
        return await self.repository.get_with_filter(
            user=user,
            session=session,
            limit=page_size,
            offset=page_number,
            filtered_schema=filter_schema,
            without_deleted=without_deleted,
        )

    @transactional
    async def is_entity_exist(
            self,
            id: int,
            *,
            session: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Предикативная функция проверки существования объекта
        :param id: id объекта
        :return: bool
        """
        return await self.repository.is_entity_exist(id=id, session=session)

    @transactional
    async def is_every_exist(
            self,
            ids: List[int],
            *,
            session: Optional[AsyncSession] = None,
    ) -> bool:
        """
        Предикат проверки множества объектов на существование
        :param id_array: Список id'шек объектов которые нужно проверить
        :return:
        """
        return await self.repository.is_every_exist(ids=ids, session=session)

    @transactional
    async def hard_delete(
            self,
            ids: List[int],
            *,
            session: Optional[AsyncSession] = None,
    ):
        await self.repository.hard_delete(ids=ids, session=session)
