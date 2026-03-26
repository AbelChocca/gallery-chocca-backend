from app.api.v1.user.user_route import router
from app.api.security.rate_limiter.ratelimiter import limiter
from app.api.dependencies.user.case_depends import get_login_user_case
from app.api.schemas.user.user_schema import LoginUserSchema
from app.api.schemas.user.mapper import InputSchemaMapper

from app.application.user.cases.login_user import LoginUserCase

from fastapi import status, Depends
from typing import Dict

@router.post(
    path='/login',
    dependencies=[Depends(limiter.limiter(limit=10, window=60))],
    status_code=status.HTTP_200_OK,
    summary='Login endpoint'
)
async def login(
    login_schema: LoginUserSchema,
    case: LoginUserCase = Depends(get_login_user_case)
) -> Dict[str, str]:
    command = InputSchemaMapper.to_login_command(login_schema)
    return await case.execute(command)