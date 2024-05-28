from typing import List, Optional

from src.features.task.schemas.task_schema_update import TaskSchemaUpdate
from src.features.task.schemas.type_of_assigner_schema import TypeOfAssignerSchema


class TaskSchemaUpdateAssigner(TaskSchemaUpdate):
    assigners: List[TypeOfAssignerSchema] | None
    observers: List[TypeOfAssignerSchema] | None
