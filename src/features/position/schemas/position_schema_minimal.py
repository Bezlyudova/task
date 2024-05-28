from src.base.base_schemas import BaseSchema
from src.features.department.schemas.department_schema_minimal import DepartmentSchemaMinimal


class PositionSchemaMinimal(BaseSchema):
    name: str
    department: DepartmentSchemaMinimal | None = None
