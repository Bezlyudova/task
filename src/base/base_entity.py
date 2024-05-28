from sqlalchemy import DateTime, ForeignKey

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class BaseEntity(Base):
    """Базовые поля в каждой модели"""

    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    create_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    write_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    create_id: Mapped[int] = mapped_column(ForeignKey("employee.id"), nullable=True)
    writer_id: Mapped[int] = mapped_column(ForeignKey("employee.id"), nullable=True)
    delete_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=None, nullable=True
    )
    deleter_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id"), server_default=None, nullable=True
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)

