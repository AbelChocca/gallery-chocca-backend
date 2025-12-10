from app.modules.user.interface.user_route import router
from app.modules.user.interface.schema.schema import ReadUser
from app.modules.user.interface.dependencies.case_depends import get_check_admin_session_case
from app.modules.user.interface.schema.schema_entity_mapper import SchemaEntityMapper

from app.modules.user.domain.cases.check_admin_session import CheckAdminSessionCase

from fastapi import status, Depends

@router.get(
    path='/admin',
    status_code=status.HTTP_200_OK,
    response_model=ReadUser,
    summary="Endpoint for check admin session"
)
async def get_info(
    user_case: CheckAdminSessionCase = Depends(get_check_admin_session_case)
) -> ReadUser:
    admin = await user_case.execute()
    return SchemaEntityMapper.to_schema(admin)