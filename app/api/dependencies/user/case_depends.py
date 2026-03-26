from app.application.user.cases.register_user import RegisterUserCase
from app.application.user.cases.login_user import LoginUserCase
from app.application.user.cases.logout_user import LogoutUserCase
from app.application.user.cases.get_users import GetUsersCase
from app.application.user.cases.get_user_by_id import GetUserByIDCase

from fastapi import Depends

from app.api.dependencies.user.service import get_user_service
from app.application.user.service import UserService

# dependencies
def get_register_user_case(
    user_service: UserService = Depends(get_user_service)
) -> RegisterUserCase:
    return RegisterUserCase(user_service)

def get_login_user_case(
    user_service: UserService = Depends(get_user_service)
) -> LoginUserCase:
    return LoginUserCase(user_service)

def get_logout_user_case(
    user_service: UserService = Depends(get_user_service)
) -> LogoutUserCase:
    return LogoutUserCase(user_service)

def get_users_case(
    user_service: UserService = Depends(get_user_service)
) -> GetUsersCase:
    return GetUsersCase(user_service=user_service)

def get_user_by_id_case(
    user_service: UserService = Depends(get_user_service)
) -> GetUserByIDCase:
    return GetUserByIDCase(user_service)