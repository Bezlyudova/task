from pydantic import BaseModel


class PositionSchemaCreate(BaseModel):
    name: str
    department_id: int
