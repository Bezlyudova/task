from pydantic import BaseModel


class TaskSchemaFilter(BaseModel):
    name: str | None
