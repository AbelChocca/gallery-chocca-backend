from app.api.v1.user.user_route import router
from app.api.dependencies.user.case_depends import get_logout_user_case

from app.application.user.cases.logout_user import LogoutUserCase

from fastapi import status, Depends

@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    summary='Logout endpoint for users'
)
async def logout(
    case: LogoutUserCase = Depends(get_logout_user_case)
) -> dict:
    return await case.execute()