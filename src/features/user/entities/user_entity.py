# from typing import Optional
#
# from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship, Mapped, mapped_column
#
# from src.base.base_entity import BaseEntity
#
#
# class User(SQLAlchemyBaseUserTable[int], BaseEntity):
#     employee_id: Mapped[Optional[int]] = mapped_column(
#         ForeignKey("employee.id"), nullable=True
#     )
#     employee = relationship(
#         "Employee", foreign_keys=[employee_id], uselist=False
#     )
#
