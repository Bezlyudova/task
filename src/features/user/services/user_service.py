# from fastapi import Depends
# from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
#
# from src.base.base_service import BaseService, BaseRepository, AsyncSession
# from src.features.user.entities import User
#
#
# class UserService(BaseService):
#     @property
#     def repository(self) -> BaseRepository:
#         return BaseRepository(self.req)
#
# # @tra
# # async def get_user_db(session: AsyncSession = Depends(get_async_session)):
# #     yield SQLAlchemyUserDatabase(session, User)
