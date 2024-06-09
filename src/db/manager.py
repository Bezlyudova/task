from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from src.db.auth import auth_backend
from src.db.session import get_session
from src.features.employee.entities.employee_entity import Employee

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[Employee, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: Employee, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    # async def on_after_forgot_password(
    #     self, user: User, token: str, request: Optional[Request] = None
    # ):
    #     print(f"User {user.id} has forgot their password. Reset token: {token}")
    #
    # async def on_after_request_verify(
    #     self, user: User, token: str, request: Optional[Request] = None
    # ):
    #     print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager():
    new_session = await anext(get_session())
    async with new_session.begin() as session:
        yield UserManager(SQLAlchemyUserDatabase(session, Employee))


fastapi_users = FastAPIUsers[Employee, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
