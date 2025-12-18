from app.api.v1.user.user_route import router
from app.api.dependencies.user.case_depends import get_login_user_case
from app.api.schemas.user.schema_model import LoginUserSchema
from app.api.schemas.user.mapper import InputSchemaMapper

from app.application.user.cases.login_user import LoginUserCase
from app.application.user.commands import LoginUserCommand

from fastapi import status, Depends
from typing import Dict

@router.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    summary='Login endpoint'
)
async def login(
    login_schema: LoginUserSchema,
    case: LoginUserCase = Depends(get_login_user_case)
) -> Dict[str, str]:
    command: LoginUserCommand = InputSchemaMapper.to_login_command(login_schema)
    return await case.execute(command)