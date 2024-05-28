from typing import List

from src.features.task.schemas.task_schema_create import TaskSchemaCreate
from src.features.task.schemas.type_of_assigner_schema import TypeOfAssignerSchema


class TaskSchemaCreateAssigner(TaskSchemaCreate):
    assigners: List[TypeOfAssignerSchema]
    observers: List[TypeOfAssignerSchema]
