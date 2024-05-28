from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel


class BaseSchema(BaseModel):
    id: Optional[int]

    class Config:
        use_enum_values = True
        from_attributes = True


SchemaType = TypeVar("SchemaType", bound=BaseSchema)


class BasePaginationSchema(GenericModel, Generic[SchemaType]):
    limit: int
    offset: int
    total: int
    data: List[SchemaType]
