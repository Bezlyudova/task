from datetime import datetime

from pydantic import BaseModel


class TaskSchemaFilter(BaseModel):
    name: str | None
    dead_line_date: datetime | None
