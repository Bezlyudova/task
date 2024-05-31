from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Path

from src.base.base_schemas import BasePaginationSchema
from src.features.employee.schemas.employee_schema import EmployeeSchema
from src.features.employee.schemas.employee_schema_create import EmployeeSchemaCreate
from src.features.employee.schemas.employee_schema_filter import EmployeeSchemaFilter
from src.features.employee.schemas.employee_schema_minimal import EmployeeSchemaMinimal
from src.features.employee.schemas.employee_schema_update import EmployeeSchemaUpdate
from src.features.employee.services.employee_service import EmployeeService

router = APIRouter(prefix="/api/employee", tags=["employee"])

@router.get("/me/")
async def get_account(
    service=Depends(EmployeeService),
):
    return await service.get_by_id_without_activity(id=1)

@router.get("/login/")
async def login(
    service=Depends(EmployeeService),
    login: Optional[str] = Query(
        None,
        example="zubenko@belmail.by",
        description="Email",
    ),
    password: Optional[str] = Query(
        None,
        example="zubenko@belmail.by",
        description="Email",
    ),
) -> EmployeeSchema:
    return await service.login(login=login)

@router.get("/logout/")
async def logout(
    service=Depends(EmployeeService),
):
    return "До скорых встреч!"

@router.post("/")
async def create(
        schema_create: EmployeeSchemaCreate,
        service=Depends(EmployeeService),
) -> EmployeeSchema:
    return await service.create(schema_create=schema_create)


@router.get("/{id}")
async def get_by_id(
        id: int = Path(example=10, description="ID искомого работника"),
        service=Depends(EmployeeService),
) -> EmployeeSchema:
    return await service.get_by_id(id=id)


@router.patch("/{id}")
async def update(
        schema_update: EmployeeSchemaUpdate,
        id: int = Path(example=10, description="ID работника, который должен быть изменен"),
        service=Depends(EmployeeService),
) -> EmployeeSchema:
    return await service.update(id=id, schema_update=schema_update)


@router.delete("/{id}")
async def delete(
        id: int = Path(
            example=10, description="ID работника, который должен быть помечен как удаленный"
        ),
        service=Depends(EmployeeService),
) -> EmployeeSchema:
    return await service.soft_delete(id=id)


@router.get("/")
async def get(
        without_deleted: bool = Query(
            False,
            example=False,
            description="Надо ли вытягивать объекты помеченные как удаленные? True - надо, False - не надо",
        ),
        post: Optional[str] = Query(
            None,
            example="Инженер-программист",
            description="Полная или частичная должность работника",
        ),
        name: Optional[str] = Query(None, example="Михаил", description="Имя работника"),
        last_name: Optional[str] = Query(
            None, example="Зубенко", description="Фамилия работника"
        ),
        middle_name: Optional[str] = Query(
            None, example="Петрович", description="Отчество (если есть)"
        ),
        email: Optional[str] = Query(
            None,
            example="zubenko@belmail.by",
            description="Email",
        ),
        phone_number: Optional[str] = Query(
            None, example="+375296665533", description="Номер телефона"
        ),
        # full_name: Optional[str] = Query(None, example="Зубенко Михаил", description="ФИО"),
        position_id: int = Query(None, example=10, description="ID должности"),
        department_id: int = Query(None, example=10, description="ID департамента"),
        organisation_id: int = Query(None, example=10, description="ID организации"),
        limit: int = Query(10, example=10, description="Размер страницы"),
        page: int = Query(1, example=1, description="Номер страницы"),
        service=Depends(EmployeeService),
) -> BasePaginationSchema[EmployeeSchemaMinimal]:
    return await service.get_filtered_data(
        filter_schema=EmployeeSchemaFilter(
            post=post,
            name=name,
            last_name=last_name,
            middle_name=middle_name,
            email=email,
            phone_number=phone_number,
            # full_name=full_name,
            organisation_id=organisation_id,
            department_id=department_id,
            position_id=position_id,
        ),
        without_deleted=without_deleted,
        page_number=page,
        page_size=limit,
    )


# @router.get("/me/id")
# async def get_by_id(
#         account: Account = Depends(get_account()),
#         service=Depends(EmployeeService),
# ):
#     return {
#         "id": account.id,
#         "guid": await service.get_guid_by_empl_id(empl_id=account.id),
#     }


@router.delete("/")
async def delete_list(
        ids: List[int] = Query(default=None, example=[1, 2, 3], description="IDs"),
        service=Depends(EmployeeService),
) -> List[int]:
    await service.soft_delete_all(ids=ids)
    return ids