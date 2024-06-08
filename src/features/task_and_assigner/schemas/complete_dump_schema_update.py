from pydantic.main import BaseModel


class CompleteDumpSchemaUpdate(BaseModel):
    is_completed: bool | None
