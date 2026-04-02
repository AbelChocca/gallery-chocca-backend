from app.api.v1.user.user_route import router
from app.api.schemas.user.user_schema import RegisterUserSchema, ReadSessionSchema
from app.api.dependencies.user.case_depends import get_register_user_case
from app.api.schemas.user.mapper import InputSchemaMapper
from app.application.user.cases.register_user import RegisterUserCase
from app.api.security.resolvers.session_owner import get_anon_id
from app.api.security.resolvers.captcha_resolver import verify_captcha

from fastapi import status, Depends
from typing import Annotated

@router.post(
    '/register',
    response_model=ReadSessionSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Register form for user'
    )
async def register_user(
    register_schema: Annotated[RegisterUserSchema, Depends(verify_captcha)],
    use_case: Annotated[RegisterUserCase,  Depends(get_register_user_case)],
    anon_id: Annotated[int, Depends(get_anon_id)]
) -> ReadSessionSchema:
    command = InputSchemaMapper.to_register_command(register_schema)
    dto_res = await use_case.exec(command, anon_id)
    return ReadSessionSchema(**dto_res)