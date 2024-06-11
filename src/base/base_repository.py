import datetime
import enum
from abc import abstractmethod, ABC
from itertools import chain
from typing import TypeVar, Type, List

from fastapi import Request
from pydantic import BaseModel
from sqlalchemy import (
    select,
    func,
    update,
    inspect,
    delete,
    distinct,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.base.base_entity import BaseEntity
from src.base.base_exception import BaseExceptionCustom
from src.base.base_schemas import BaseSchema, BasePaginationSchema

ModelType = TypeVar("ModelType", bound=BaseEntity)
SchemaType = TypeVar("SchemaType", bound=BaseSchema)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
MinimalSchemaType = TypeVar("MinimalSchemaType", bound=BaseSchema)
FilterSchemaType = TypeVar("FilterSchemaType", bound=BaseModel)


class BaseRepo(
    #             entity     | dto      | dto_create    | dto_update       |  dto_minimal
    ABC,
):
    @property
    @abstractmethod
    def model(self) -> Type[ModelType]:
        raise NotImplemented("Абстрактный метод не реализован")

    def __init__(self, req: Request):
        self.request = req

    """
    ModelType - Модель sqlalchemy
    SchemaType - Схема Pydentic
    CreateSchemaType - Данные которые необходимы для создания записи
    UpdateSchemaType - Данные для обновления
    MinimalSchemaType - Минимальные данные для табличных представлений на фронте
    """

    @property
    @abstractmethod
    def schema(self) -> Type[SchemaType]:
        raise NotImplemented("Абстрактный метод не реализован")

    @property
    @abstractmethod
    def create_schema(self) -> Type[CreateSchemaType]:
        raise NotImplemented("Абстрактный метод не реализован")

    @property
    @abstractmethod
    def update_schema(self) -> Type[UpdateSchemaType]:
        raise NotImplemented("Абстрактный метод не реализован")

    @property
    @abstractmethod
    def minimal_schema(self) -> Type[MinimalSchemaType]:
        raise NotImplemented("Абстрактный метод не реализован")

    @property
    @abstractmethod
    def filter_schema(self) -> Type[FilterSchemaType]:
        raise NotImplemented("Абстрактный метод не реализован")

    @property
    def common_options(self):
        return [
            (
                joinedload(i),
                # with_loader_criteria(
                #     i.entity.class_, i.entity.class_.is_deleted != True
                # ),
            )
            for i in inspect(self.model).relationships.values()
        ]

    def transform(self, data: ModelType) -> SchemaType:
        return self.schema.from_orm(data)

    def transform_minimal(self, data: ModelType) -> MinimalSchemaType:
        return self.minimal_schema.from_orm(data)

    def transform_many(self, data: list[ModelType]) -> list[SchemaType]:
        return [self.transform(item) for item in data]

    def transform_many_minimal(self, data: List[ModelType]) -> list[MinimalSchemaType]:
        return [self.transform_minimal(item) for item in data]

    async def create(
        self,
        session: AsyncSession,
        schema_create: CreateSchemaType,
    ) -> SchemaType:
        return await self.create_system(session=session, schema_create=schema_create)

    async def create_system(
        self,
        session: AsyncSession,
        schema_create: CreateSchemaType,
    ) -> SchemaType:
        """
        Метод для создания записей
        :param session: sqlalchemy session abstraction
        :param schema_create: Данные необходимые для создания записи
        :return: Новая запись
        """
        new_entity = self.model(**schema_create.dict())
        new_entity.writer_id = 1
        # new_entity.create_id = 1

        session.add(new_entity)
        new_entity.create_date = datetime.datetime.now()
        await session.flush()
        return self.schema(**new_entity.__dict__)

    async def get_by_id_without_activity(
        self, session: AsyncSession, id: int, without_deleted=True
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
        if self.special_filter() is not None:
            where_options.append(self.special_filter())
        res = (await session.execute(req.where(*where_options))).scalar()
        if res is None:
            from src.base.base_exception import BaseExceptionCustom
            raise BaseExceptionCustom(
                status_code=404,
                reason=f"{self.model.__name__} with current ID: < {id} > was not found",
                message=f"Объект не найден",
            )
        return self.schema.from_orm(res)

    async def get_by_id(
        self, session: AsyncSession, id: int, without_deleted=True
    ) -> SchemaType:
        return await self.get_by_id_without_activity(
            session=session, id=id, without_deleted=without_deleted
        )

    async def get_entity_by_id(
        self, session: AsyncSession, id: int, without_deleted=True
    ) -> SchemaType:
        res = (
            await session.execute(
                select(self.model)
                .options(*chain(*self.common_options))
                .where(self.model.is_deleted != without_deleted, self.model.id == id)
            )
        ).scalar()
        return res

    async def update(
        self, session: AsyncSession, id: int, schema_update: update_schema
    ) -> SchemaType:
        """
        Обновление
        :param session: sqlalchemy session abstraction
        :param id: id записи
        :param schema_update: Данные для обновления
        :return: Обновленный объект
        """
        await session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(schema_update.dict(exclude_unset=True))
        )
        return await self.get_by_id_without_activity(session=session, id=id)

    async def soft_delete(self, session: AsyncSession, id: int) -> SchemaType:
        """
        Мягкое удаление
        :param session:sqlalchemy session abstraction
        :param id: id удаляемого объекта
        :param deleter_id:
        :return:
        """

        result = await self.get_by_id_without_activity(session=session, id=id, without_deleted=True)
        await session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(
                {
                    "is_deleted": True,
                    "deleter_id": 1,
                    "delete_date": datetime.datetime.now(),
                    "writer_id": 1,
                }
            )
        )

        return result

    async def soft_delete_all(self, session: AsyncSession, ids: List[int]) -> bool:
        """
        Мягкое удаление
        :param session:sqlalchemy session abstraction
        :param ids: id удаляемых объектов
        :param deleter_id:
        :return:
        """

        await session.execute(
            update(self.model)
            .where(self.model.id.in_(ids))
            .values(
                {
                    "is_deleted": True,
                    "deleter_id": 1,
                    "delete_date": datetime.datetime.now(),
                    "writer_id": 1,
                }
            )
        )

        return True

    async def is_deleted(self, session, id: int):
        res = await session.get(self.model, id)

        if res is None:
            raise BaseExceptionCustom(
                status_code=404,
                reason=f"{self.model.__name__ } with current ID: < {id} > was not found",
                message=f"Объект не найден",
            )
        return res.is_deleted

    async def get_count(self, session: AsyncSession, custom_query=None) -> int:
        """
        Метод для подсчета кол-ва записей
        :param session: sqlalchemy session abstraction
        :param custom_query: Условие для которого считаем кол-во записей
        :return: int кол-во записей
        """

        query = select(func.count(distinct(self.model.id)))
        if custom_query is not None:
            if isinstance(custom_query, list | tuple):
                query = query.where(*custom_query)
            else:
                query = query.where(custom_query)
        res = (await session.execute(query)).scalar()

        return res or 0

    def special_filter(self):
        return None

    def get_filter_query(self, filter_schema, without_deleted):
        data_query = []
        if self.special_filter() is not None:
            data_query.append(self.special_filter())

        for k, v in filter_schema.dict(exclude_unset=True).items():
            if v is not None and k in self.model.__dict__.keys():
                if isinstance(v, str):
                    data_query.append(
                        self.model.__getattribute__(self.model, k).ilike(f"%{str(v)}%")
                    )
                # elif isinstance(v, int) or isinstance(v, enum.Enum) or isinstance(v, datetime.datetime):
                elif isinstance(v, int) or isinstance(v, enum.Enum):
                    data_query.append(self.model.__getattribute__(self.model, k) == v)

                elif isinstance(v, list):
                    if v[0]:
                        data_query.append(
                            self.model.__getattribute__(self.model, k).in_(v)
                        )

        if not without_deleted:
            data_query.append(self.model.is_deleted.is_(False))

        return data_query

    async def get_with_filter(
        self,

        session: AsyncSession,
        limit: int,
        offset: int,
        filtered_schema,
        without_deleted=True,
    ) -> BasePaginationSchema[MinimalSchemaType]:
        query_filter = self.get_filter_query(
            filter_schema=filtered_schema, without_deleted=without_deleted
        )
        data_query = session.execute(
            select(self.model)
            .options(*chain(*self.common_options))
            .limit(limit)
            .offset((offset - 1) * limit)
            .where(*query_filter)
        )
        data = await data_query
        count = await self.get_count(session, query_filter)
        data = self.transform_many_minimal(data.scalars().unique())

        data = BasePaginationSchema[self.minimal_schema](
            total=count, data=data, limit=limit, offset=offset
        )
        return data

    async def hard_delete(self, ids: List[int], session: AsyncSession):
        await session.execute(delete(self.model).where(self.model.id.in_(ids)))

    async def hard_delete_all(self, ids: List[int], session: AsyncSession):
        await session.execute(delete(self.model).where(self.model.id.in_(ids)))
