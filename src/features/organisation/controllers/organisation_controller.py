from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Path

from src.base.base_schemas import BasePaginationSchema
from src.db.manager import current_user
from src.features.employee.entities.employee_entity import Employee
from src.features.organisation.schemas.organisation_schema import OrganisationSchema
from src.features.organisation.schemas.organisation_schema_create import OrganisationSchemaCreate
from src.features.organisation.schemas.organisation_schema_filter import OrganisationSchemaFilter
from src.features.organisation.schemas.organisation_schema_minimal import OrganisationSchemaMinimal
from src.features.organisation.schemas.organisation_schema_update import OrganisationSchemaUpdate
from src.features.organisation.services.organisation_service import OrganisationService

router = APIRouter(prefix="/api/organisation", tags=["organisation"])


@router.post("/")
async def create(
        schema_create: OrganisationSchemaCreate,
        service=Depends(OrganisationService),
        user: Employee = Depends(current_user)
) -> OrganisationSchema:
    return await service.create(user=user, schema_create=schema_create)


@router.get("/{id}")
async def get_by_id(
        id: int = Path(example=10, description="ID искомой организации"),
        service=Depends(OrganisationService),
        user: Employee = Depends(current_user)
) -> OrganisationSchema:
    return await service.get_by_id(user=user, id=id)


@router.patch("/{id}")
async def update(
        schema_update: OrganisationSchemaUpdate,
        id: int = Path(example=10, description="ID организации, которая должна быть изменена"),
        service=Depends(OrganisationService),
        user: Employee = Depends(current_user)
) -> OrganisationSchema:
    return await service.update(user=user, id=id, schema_update=schema_update)


@router.delete("/{id}")
async def delete(
        id: int = Path(
            example=10, description="ID организации, которая должна быть помечена как удаленная"
        ),
        service=Depends(OrganisationService),
        user: Employee = Depends(current_user)
) -> OrganisationSchema:
    return await service.soft_delete(user=user, id=id)


@router.get("/")
async def get(
        without_deleted: bool = Query(
            False,
            example=False,
            description="Надо ли вытягивать объекты помеченные как удаленные? True - надо, False - не надо",
        ),
        phone_number: Optional[str] = Query(
            None, example="+375296665533", description="Номер телефона"
        ),
        name: Optional[str] = Query(
            None, example="ОблГаз", description="Название внутренней организации"
        ),
        note: Optional[str] = Query(
            None,
            example="Наша главная организация, которая кормит нас",
            description="Описание или записка",
        ),
        limit: int = Query(10, example=10, description="Размер страницы"),
        page: int = Query(1, example=1, description="Номер страницы"),
        service=Depends(OrganisationService),
        user: Employee = Depends(current_user)
) -> BasePaginationSchema[OrganisationSchemaMinimal]:
    return await service.get_filtered_data(
        user=user,
        filter_schema=OrganisationSchemaFilter(
            name=name,
            phone_number=phone_number,
            note=note,
        ),
        without_deleted=without_deleted,
        page_number=page,
        page_size=limit,
    )


@router.delete("/")
async def delete_list(
        ids: List[int] = Query(default=None, example=[1, 2, 3], description="IDs"),
        service=Depends(OrganisationService),
        user: Employee = Depends(current_user)
) -> List[int]:
    await service.soft_delete_all(user=user, ids=ids)
    return ids
