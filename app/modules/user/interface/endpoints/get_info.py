from app.modules.user.interface.user_route import router
from app.modules.user.interface.schema.schema import ReadUser
from app.modules.user.interface.dependencies.case_depends import get_check_user_session_case
from app.modules.user.interface.schema.schema_entity_mapper import SchemaEntityMapper

from app.modules.user.domain.cases.check_session import CheckUserSessionCase

from fastapi import status, Depends

@router.get(
    path='/me',
    status_code=status.HTTP_200_OK,
    response_model=ReadUser,
    summary="Endpoint for user's info"
)
async def get_info(
    user_case: CheckUserSessionCase = Depends(get_check_user_session_case)
) -> ReadUser:
    user = await user_case.execute()
    return SchemaEntityMapper.to_schema(user)