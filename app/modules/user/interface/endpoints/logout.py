from app.modules.user.interface.user_route import router
from app.modules.user.interface.dependencies.case_depends import get_logout_user_case

from app.modules.user.domain.cases.logout_user import LogoutUserCase

from fastapi import status, Request, Response, Depends


@router.post(
    path='/logout',
    status_code=status.HTTP_200_OK,
    summary='Logout endpoint for users'
)
async def logout(
    case: LogoutUserCase = Depends(get_logout_user_case)
) -> dict:
    return await case.execute()