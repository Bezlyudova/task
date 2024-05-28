from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.base.base_entity import BaseEntity
from src.entity_type import TypeOfEntity


class Position(BaseEntity):
    __tablename__ = "position"

    name: Mapped[str] = mapped_column(String(400), nullable=True)

    department_id: Mapped[int] = mapped_column(
        ForeignKey("department.id"), nullable=True
    )
    department = relationship(
        "Department",
        foreign_keys=[department_id],
    )
    entity_type: TypeOfEntity = TypeOfEntity.POSITION
