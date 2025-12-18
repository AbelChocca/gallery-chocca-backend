from app.api.v1.user.user_route import router
from app.api.schemas.user.schema_model import ReadUserSchema
from app.api.schemas.user.mapper import OutputSchemaMapper
from app.api.dependencies.user.case_depends import get_check_admin_session_case

from app.application.user.cases.check_admin_session import CheckAdminSessionCase

from fastapi import status, Depends

@router.get(
    path='/admin',
    status_code=status.HTTP_200_OK,
    response_model=ReadUserSchema,
    summary="Endpoint for check admin session"
)
async def get_info(
    user_case: CheckAdminSessionCase = Depends(get_check_admin_session_case)
) -> ReadUserSchema:
    admin_dto = await user_case.execute()
    return OutputSchemaMapper.to_read_schema(admin_dto)