from app.api.v1.user.user_route import router
from app.api.schemas.user.schema_model import ReadUserSchema
from app.api.dependencies.user.case_depends import get_check_user_session_case
from app.api.schemas.user.mapper import OutputSchemaMapper

from app.application.user.cases.check_session import CheckUserSessionCase

from fastapi import status, Depends

@router.get(
    path='/me',
    status_code=status.HTTP_200_OK,
    response_model=ReadUserSchema,
    summary="Endpoint for user's info"
)
async def get_info(
    user_case: CheckUserSessionCase = Depends(get_check_user_session_case)
) -> ReadUserSchema:
    user_dto = await user_case.execute()
    return OutputSchemaMapper.to_read_schema(user_dto)