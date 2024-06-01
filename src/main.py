import asyncio

from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.base.base_exception import BaseExceptionCustom
from src.db.auth import auth_backend
from src.db.manager import fastapi_users
from src.db.session import get_session
from src.features.department.controllers import department_controller
from src.features.employee.controllers import employee_controller
from src.features.employee.schemas.employee_schema import EmployeeSchema
from src.features.employee.schemas.employee_schema_create import EmployeeSchemaCreate
from src.features.organisation.controllers import organisation_controller
from src.features.position.controllers import position_controller
from src.features.task.controllers import task_controller
from src.features.task.services.task_service import TaskService
from apscheduler.schedulers.asyncio import AsyncIOScheduler


app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(department_controller.router)
app.include_router(employee_controller.router)
app.include_router(organisation_controller.router)
app.include_router(position_controller.router)
app.include_router(task_controller.router)

# fastapi_users = FastAPIUsers[Employee, int](
#     get_user_manager,
#     [auth_backend],
# )
#
# current_user = fastapi_users.current_user()

#
# @app.get("/protected-route")
# def protected_route():
#     return f"Hello, {user.email}"


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/docs/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(EmployeeSchema, EmployeeSchemaCreate),
    prefix="/api/docs/auth",
    tags=["auth"],
)

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job("interval", minutes=10)
async def check_deadline():
    await asyncio.create_task(
        TaskService(
            req=None, session=await anext(get_session())
        ).check_deadline(session=None)
    )


@app.exception_handler(BaseExceptionCustom)
async def validation_exception_handler(request, err: BaseExceptionCustom):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    # Change here to LOGGER
    return JSONResponse(
        status_code=err.status_code,
        content={"reason": f"{err.reason}", "message": f"{err.message}"},
    )
# if __name__ == "__main__":
#     uvicorn.run(app, loop="auto")