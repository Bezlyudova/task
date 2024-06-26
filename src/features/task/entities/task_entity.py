from sqlalchemy import DateTime, ForeignKey, Enum, Integer
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.base.base_entity import BaseEntity
from src.entity_type import TypeOfEntity
from src.task_state_enum import TaskStateEnum


class Task(BaseEntity):
    __tablename__ = "task"

    name: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String(1000), nullable=True)

    dead_line_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), index=True
    )

    is_expired: Mapped[bool] = mapped_column(default=False)
    expired_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    state: Mapped[TaskStateEnum] = mapped_column(
        Enum(TaskStateEnum), server_default=TaskStateEnum.DRAFT.name
    )
    started_by: Mapped[int] = mapped_column(ForeignKey("employee.id"), nullable=True)
    started = relationship("Employee", foreign_keys=started_by)

    start_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    is_completed: Mapped[bool] = mapped_column(default=False)
    completed_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    priority: Mapped[int] = mapped_column(Integer, default=0, nullable=True)

    assigners = relationship("TaskAndAssigner")
    entity_type: TypeOfEntity = TypeOfEntity.TASK
