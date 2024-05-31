from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Path

from src.base.base_schemas import BasePaginationSchema
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
) -> PositionSchema:
    return await service.create(schema_create=schema_create)


@router.get("/{id}")
async def get_by_id(
        id: int = Path(example=10, description="ID искомой должности"),
        service=Depends(PositionService),
) -> PositionSchema:
    return await service.get_by_id(id=id)


@router.patch("/{id}")
async def update(
        schema_update: PositionSchemaUpdate,
        id: int = Path(example=10, description="ID должности, которая должен быть изменена"),
        service=Depends(PositionService),
) -> PositionSchema:
    return await service.update(id=id, schema_update=schema_update)


@router.delete("/{id}")
async def delete(
        id: int = Path(
            example=10, description="ID должности, которая должен быть помечена как удаленная"
        ),
        service=Depends(PositionService),
) -> PositionSchema:
    return await service.soft_delete(id=id)


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
) -> BasePaginationSchema[PositionSchemaMinimal]:
    return await service.get_filtered_data(
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
) -> List[int]:
    await service.soft_delete_all(ids=ids)
    return ids
