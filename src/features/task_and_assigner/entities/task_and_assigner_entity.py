from sqlalchemy import DateTime, ForeignKey, Enum
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.base.base_entity import BaseEntity
from src.entity_type import TypeOfEntity
from src.type_of_assigner import TypeOfAssigner


class TaskAndAssigner(BaseEntity):
    __tablename__ = "task_and_assigner"

    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"), nullable=False)

    is_read: Mapped[bool] = mapped_column(default=False)
    read_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    is_completed: Mapped[bool] = mapped_column(default=False)
    complete_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    is_expired: Mapped[bool] = mapped_column(default=False)
    expired_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    type_of_assigner: Mapped[TypeOfAssigner] = mapped_column(
        Enum(TypeOfAssigner), index=True
    )

    note: Mapped[str] = mapped_column(String(3000), nullable=True)

    employee = relationship("Employee", foreign_keys=[employee_id])

    entity_type: TypeOfEntity = TypeOfEntity.TASK_AND_ASSIGNER
