from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.base.base_exception import BaseExceptionCustom
from src.db.auth import auth_backend
from src.db.manager import fastapi_users
from src.features.department.controllers import department_controller
from src.features.employee.controllers import employee_controller
from src.features.employee.schemas.employee_schema import EmployeeSchema
from src.features.employee.schemas.employee_schema_create import EmployeeSchemaCreate
from src.features.organisation.controllers import organisation_controller
from src.features.position.controllers import position_controller
from src.features.task.controllers import task_controller

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
# def protected_route(user: Employee = Depends(current_user)):
#     return f"Hello, {user.email}"


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(EmployeeSchema, EmployeeSchemaCreate),
    prefix="/auth",
    tags=["auth"],
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