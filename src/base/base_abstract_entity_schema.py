from pydantic.main import BaseModel

from src.entity_type import TypeOfEntity


class BaseAbstractEntitySchema(BaseModel):
    entity_id: int
    entity_type: TypeOfEntity
