from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.base.base_entity import BaseEntity
from src.entity_type import TypeOfEntity
from src.features.employee.entities.employee_entity import Employee


class Department(BaseEntity):
    __tablename__ = "department"

    name: Mapped[str] = mapped_column(String(250))
    phone_number: Mapped[str] = mapped_column(String(20))

    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"))
    organisation = relationship("Organisation", overlaps="departments")

    # employees = relationship(
    #     "Employee",
    #     primaryjoin=Employee.department_id == id,
    #     overlaps="department",
    # )

    entity_type: TypeOfEntity = TypeOfEntity.DEPARTMENT

    positions = relationship("Position", overlaps="department")

    master_id: Mapped[int] = mapped_column(ForeignKey("employee.id"), nullable=True)

    master = relationship("Employee", foreign_keys=master_id)

