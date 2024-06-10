from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query

from src.base.base_schemas import BasePaginationSchema
from src.features.task.schemas.task_schema import TaskSchema
from src.features.task.schemas.task_schema_create_assigner import TaskSchemaCreateAssigner
from src.features.task.schemas.task_schema_filter_extended import TaskSchemaFilterExtended
from src.features.task.schemas.task_schema_minimal import TaskSchemaMinimal
from src.features.task.schemas.task_schema_update_assigners import TaskSchemaUpdateAssigner
from src.features.task.services.task_service import TaskService
from src.features.task_and_assigner.schemas.complete_dump_schema_update import CompleteDumpSchemaUpdate
from src.features.task_and_assigner.schemas.read_dump_schema_update import ReadDumpSchemaUpdate
from src.task_state_enum import TaskStateEnum

router = APIRouter(prefix="/api/task", tags=["task"])


@router.get("/check_deadline/")
async def check_deadline(
    service=Depends(TaskService),
):
    return await service.check_deadline()


@router.post("/", response_model=TaskSchema)
async def create(
    create_schema: TaskSchemaCreateAssigner,
    service=Depends(TaskService),
) -> TaskSchema:
    return await service.create(schema_create=create_schema)


@router.get("/{id}", response_model=TaskSchema)
async def get_by_id(
    id: int = Path(example=10, description="ID искомой задачи"),
    service=Depends(TaskService),
) -> TaskSchema:
    return await service.get_by_id(id=id)


@router.patch("/{id}")
async def update(
    update_schema: TaskSchemaUpdateAssigner,
    id: int = Path(example=10, description="ID задачи которая будет обновлена"),
    service=Depends(TaskService),
) -> TaskSchema:
    return await service.update(id=id, schema_update=update_schema)


@router.delete("/")
async def delete_list(
    ids: List[int] = Query(default=None, example=[1, 2, 3], description="IDs"),
    service=Depends(TaskService),
) -> List[int]:
    await service.soft_delete_all(ids=ids)
    return ids


@router.delete("/{id}")
async def delete(
    id: int = Path(
        example=10, description="ID задачи которая будет помечена как удаленная"
    ),
    service=Depends(TaskService),
) -> TaskSchema:
    return await service.soft_delete(id=id)


@router.get("/")
async def get(
    without_deleted: bool = Query(
        False,
        example=False,
        description="Надо ли вытягивать объекты помеченные как удаленные? True - надо, False - не надо",
    ),
    name: Optional[str] = Query(
        None, example="Отослать письмо", description="Название задачи"
    ),
    assigner_id: Optional[int] = Query(
        None, example="1", description="Кто исполнитель"
    ),
    observer_id: Optional[int] = Query(
        None, example="1", description="Кто наблюдатель"
    ),
    create_id: Optional[int] = Query(
        None, example="1", description="Кто создатель"
    ),
    states: List[TaskStateEnum] = Query(
        None,
        example=["WORKS", "DRAFT"],
        description="Список приемлемых статусов",
    ),
    dead_line_date: Optional[datetime] = Query(datetime.now()),
    limit: int = Query(10, example=10, description="Размер страницы"),
    page: int = Query(1, example=1, description="Номер страницы"),
    service=Depends(TaskService),
) -> BasePaginationSchema[TaskSchemaMinimal]:
    return await service.get_filtered_data(
        filter_schema=TaskSchemaFilterExtended(
            name=name,
            assigner_id=assigner_id,
            observer_id=observer_id,
            create_id=create_id,
            state=states,
            # dead_line_date=dead_line_date,
        ),
        without_deleted=without_deleted,
        page_number=page,
        page_size=limit,
    )


@router.get("/assignedToMe/unreaded/")
async def get_count_unreaded_task(
    service=Depends(TaskService),
) -> int:
    return await service.get_count_unreaded_task()


@router.patch("/{task_id}/read/assigner")
async def read_assigner_task_status(
    update_schema: ReadDumpSchemaUpdate,
    task_id: int = Path(example=10, description="ID задачи"),
    service=Depends(TaskService),
) -> TaskSchema:
    return await service.read_assigner_task_status(task_id, update_schema)


@router.patch("/{task_id}/complete/assigner")
async def complete_task_for_assigner(
    update_schema: CompleteDumpSchemaUpdate,
    task_id: int = Path(example=10, description="ID задачи"),
    service=Depends(TaskService),
) -> TaskSchema:
    return await service.complete_task_for_assigner(task_id, update_schema)


@router.post("/startTask/")
async def start_task(
    task_id: int = Query(1, example=1, description="ID стартуемой таски"),
    service=Depends(TaskService),
):
    return await service.start_task(task_id)


@router.patch("/completeTask/")
async def complete_task(
    task_id: int = Query(
        1, example=1, description="ID завершаемой (помечаем как ВЫПОЛНЕННАЯ) таски"
    ),
    service=Depends(TaskService),
):
    return await service.complete_task_for_all(task_id)
