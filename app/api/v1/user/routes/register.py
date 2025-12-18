from app.api.v1.user.user_route import router
from app.api.schemas.user.schema_model import RegisterUserSchema, ReadUserSchema
from app.api.dependencies.user.case_depends import get_register_user_case
from app.api.schemas.user.mapper import InputSchemaMapper, OutputSchemaMapper
from app.application.user.cases.register_user import RegisterUserCase

from fastapi import status, Depends

@router.post(
    '/register',
    response_model=ReadUserSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Register form for user'
    )
async def register_user(
    register_schema: RegisterUserSchema,
    use_case: RegisterUserCase = Depends(get_register_user_case)
) -> ReadUserSchema:
    command = InputSchemaMapper.to_register_command(register_schema)
    dto_res = await use_case.exec(command)
    return OutputSchemaMapper.to_read_schema(dto_res)