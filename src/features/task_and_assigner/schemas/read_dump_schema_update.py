from pydantic.main import BaseModel


class ReadDumpSchemaUpdate(BaseModel):
    is_read: bool | None
