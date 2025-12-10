from app.modules.user.interface.user_route import router
from app.modules.user.interface.dependencies.case_depends import get_login_user_case
from app.modules.user.interface.schema.schema import LoginUser
from app.modules.user.interface.schema.schema_dto_mapper import DTOUserMapper
from app.shared.dto.user_dto import LoginUserDTO

from app.modules.user.domain.cases.loging_user import LoginUserCase

from fastapi import status, Depends
from typing import Dict

@router.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    summary='Login endpoint'
)
async def login(
    login_schema: LoginUser,
    case: LoginUserCase = Depends(get_login_user_case)
) -> Dict[str, str]:
    dto: LoginUserDTO = DTOUserMapper.login_mapper(login_schema)
    return await case.execute(dto)



