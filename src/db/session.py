from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.db.config import DB_USER, DB_PASS, DB_HOST, DB_NAME

# from db.config import ConfigService
#
# config: ConfigService = ConfigService()
db_engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
    echo=False,
    max_overflow=4444,
    pool_recycle=3600,
)

class DataBaseManger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DataBaseManger, cls).__new__(cls)

            cls._instance.__session = async_sessionmaker(
                db_engine,
                autoflush=False,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        return cls._instance

    @property
    def session(self):
        return self.__session


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield DataBaseManger().session
    except Exception as e:
        raise e


async def _get_session():
    async with DataBaseManger().session.begin() as session:
        return session


def transactional(func):
    async def _transactional(
        *args,
        session=None,
        **kwargs,
    ):
        if not session:
            new_session = await anext(get_session())
            async with new_session.begin() as new_sess:
                return await func(*args, **kwargs, session=new_sess)
        return await func(*args, **kwargs, session=session)

    return _transactional
