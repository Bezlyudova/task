from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Path

from src.base.base_schemas import BasePaginationSchema
from src.db.manager import current_user
from src.features.employee.entities.employee_entity import Employee
from src.features.position.schemas.position_schema import PositionSchema
from src.features.position.schemas.position_schema_create import PositionSchemaCreate
from src.features.position.schemas.position_schema_filter import PositionSchemaFilter
from src.features.position.schemas.position_schema_minimal import PositionSchemaMinimal
from src.features.position.schemas.position_schema_update import PositionSchemaUpdate
from src.features.position.services.position_service import PositionService

router = APIRouter(prefix="/api/position", tags=["position"])


@router.post("/")
async def create(
        schema_create: PositionSchemaCreate,
        service=Depends(PositionService),
        user: Employee = Depends(current_user)
) -> PositionSchema:
    return await service.create(user=user, schema_create=schema_create)


@router.get("/{id}")
async def get_by_id(
        id: int = Path(example=10, description="ID искомой должности"),
        service=Depends(PositionService),
        user: Employee = Depends(current_user)
) -> PositionSchema:
    return await service.get_by_id(user=user, id=id)


@router.patch("/{id}")
async def update(
        schema_update: PositionSchemaUpdate,
        id: int = Path(example=10, description="ID должности, которая должен быть изменена"),
        service=Depends(PositionService),
        user: Employee = Depends(current_user)
) -> PositionSchema:
    return await service.update(user=user, id=id, schema_update=schema_update)


@router.delete("/{id}")
async def delete(
        id: int = Path(
            example=10, description="ID должности, которая должен быть помечена как удаленная"
        ),
        service=Depends(PositionService),
        user: Employee = Depends(current_user)
) -> PositionSchema:
    return await service.soft_delete(user=user, id=id)


@router.get("/")
async def get(
        without_deleted: bool = Query(
            False,
            example=False,
            description="Надо ли вытягивать объекты помеченные как удаленные? True - надо, False - не надо",
        ),
        name: Optional[str] = Query(
            None,
            example="Инженер",
            description="Частичное или полное наименование должности",
        ),
        department_id: Optional[int] = Query(
            None,
            example="2",
            description="ID подразделения",
        ),
        limit: int = Query(10, example=10, description="Размер страницы"),
        page: int = Query(1, example=1, description="Номер страницы"),
        service=Depends(PositionService),
        user: Employee = Depends(current_user)
) -> BasePaginationSchema[PositionSchemaMinimal]:
    return await service.get_filtered_data(
        user=user,
        filter_schema=PositionSchemaFilter(
            name=name,
            department_id=department_id,
        ),
        without_deleted=without_deleted,
        page_number=page,
        page_size=limit,
    )


@router.delete("/")
async def delete_list(
        ids: List[int] = Query(default=None, example=[1, 2, 3], description="IDs"),
        service=Depends(PositionService),
        user: Employee = Depends(current_user)
) -> List[int]:
    await service.soft_delete_all(user=user, ids=ids)
    return ids
