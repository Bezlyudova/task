from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.base.base_entity import BaseEntity
from src.entity_type import TypeOfEntity


class Employee(SQLAlchemyBaseUserTable[int], BaseEntity):
    __tablename__ = "employee"

    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    name: Mapped[str] = mapped_column(String(500), index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    middle_name: Mapped[str] = mapped_column(String(100), nullable=True, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)

    organisation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organisation.id"), nullable=True
    )
    department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("department.id"), nullable=True
    )
    position_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("position.id"), nullable=True
    )

    organisation = relationship(
        "Organisation", foreign_keys=[organisation_id], uselist=False
    )
    department = relationship("Department", foreign_keys=[department_id], uselist=False)

    position = relationship("Position", foreign_keys=[position_id], uselist=False)

    entity_type: TypeOfEntity = TypeOfEntity.EMPLOYEE
