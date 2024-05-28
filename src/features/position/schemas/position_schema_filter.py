from pydantic import BaseModel


class PositionSchemaFilter(BaseModel):
    name: str | None
    department_id: int | None
