from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.base.base_entity import BaseEntity
from src.entity_type import TypeOfEntity


class Organisation(BaseEntity):
    __tablename__ = "organisation"

    phone_number: Mapped[str] = mapped_column(String(200), nullable=True)
    name: Mapped[str] = mapped_column(String(500), index=True, nullable=True)
    note: Mapped[str] = mapped_column(String(1000), nullable=True)

    departments = relationship(
        "Department",
        # lazy="joined",
    )

    master_id: Mapped[int] = mapped_column(ForeignKey("employee.id"), nullable=True)

    parent_id: Mapped[int] = mapped_column(
        ForeignKey("organisation.id"), nullable=True
    )

    is_main: Mapped[bool] = mapped_column(default=False)

    master = relationship("Employee", foreign_keys=master_id)

    entity_type: TypeOfEntity = TypeOfEntity.ORGANISATION
