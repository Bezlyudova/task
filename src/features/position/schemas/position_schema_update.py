from pydantic import BaseModel


class PositionSchemaUpdate(BaseModel):
    name: str | None
    department_id: int | None
