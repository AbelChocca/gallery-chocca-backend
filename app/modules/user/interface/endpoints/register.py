from app.modules.user.interface.user_route import router
from app.modules.user.interface.schema.schema import RegisterUser, ReadUser
from app.modules.user.interface.dependencies.case_depends import get_register_user_case
from app.modules.user.interface.schema.schema_entity_mapper import SchemaEntityMapper
from app.modules.user.interface.schema.schema_dto_mapper import DTOUserMapper
from app.modules.user.domain.cases.register_user import RegisterUserCase

from fastapi import status, Depends

@router.post(
    '/register',
    response_model=ReadUser,
    status_code=status.HTTP_201_CREATED,
    summary='Register form for user'
    )
async def register_user(
    register_schema: RegisterUser,
    use_case: RegisterUserCase = Depends(get_register_user_case)
) -> ReadUser:
    dto = DTOUserMapper.register_mapper(register_schema)
    user = await use_case.exec(dto)
    return SchemaEntityMapper.to_schema(user)