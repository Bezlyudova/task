from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Path

from src.base.base_schemas import BasePaginationSchema
from src.features.department.schemas.department_schema import DepartmentSchema
from src.features.department.schemas.department_schema_create import DepartmentSchemaCreate
from src.features.department.schemas.department_schema_filter import DepartmentSchemaFilter
from src.features.department.schemas.department_schema_minimal import DepartmentSchemaMinimal
from src.features.department.schemas.department_schema_update import DepartmentSchemaUpdate
from src.features.department.services.department_service import DepartmentService

router = APIRouter(prefix="/api/department", tags=["department"])


@router.post("/")
async def create(
        schema_create: DepartmentSchemaCreate,
        service=Depends(DepartmentService),
        
) -> DepartmentSchema:
    return await service.create(schema_create=schema_create)


@router.get("/{id}")
async def get_by_id(
        id: int = Path(example=10, description="ID искомого подразделения"),
        service=Depends(DepartmentService),
) -> DepartmentSchema:
    return await service.get_by_id(id=id)


@router.patch("/{id}")
async def update(
        schema_update: DepartmentSchemaUpdate,
        id: int = Path(example=10, description="ID подразделения, которое должен быть изменено"),
        service=Depends(DepartmentService),
) -> DepartmentSchema:
    return await service.update(id=id, schema_update=schema_update)


@router.delete("/{id}")
async def delete(
        id: int = Path(
            example=10, description="ID подразделения, которое должен быть помечено как удаленное"
        ),
        service=Depends(DepartmentService),
) -> DepartmentSchema:
    return await service.soft_delete(id=id)


@router.get("/")
async def get(
        without_deleted: bool = Query(
            False,
            example=False,
            description="Надо ли вытягивать объекты помеченные как удаленные? True - надо, False - не надо",
        ),
        name: Optional[str] = Query(None, example="Витебскоблгаз", description="Название организации"),
        phone_number: Optional[str] = Query(None, example="+7542189", description="Номер телефона"),
        organisation_id: int = Query(None, example=10, description="ID организации"),
        limit: int = Query(10, example=10, description="Размер страницы"),
        page: int = Query(1, example=1, description="Номер страницы"),
        service=Depends(DepartmentService),
        
) -> BasePaginationSchema[DepartmentSchemaMinimal]:
    return await service.get_filtered_data(
        filter_schema=DepartmentSchemaFilter(
            name=name,
            phone_number=phone_number,
            organisation_id=organisation_id,
        ),
        without_deleted=without_deleted,
        page_number=page,
        page_size=limit,
    )


@router.delete("/")
async def delete_list(
        ids: List[int] = Query(default=None, example=[1, 2, 3], description="IDs"),
        service=Depends(DepartmentService),
) -> List[int]:
    await service.soft_delete_all(ids=ids)
    return ids
