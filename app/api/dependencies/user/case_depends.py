from app.application.user.cases.register_user import RegisterUserCase
from app.application.user.cases.check_session import CheckUserSessionCase
from app.application.user.cases.login_user import LoginUserCase
from app.application.user.cases.logout_user import LogoutUserCase
from app.application.user.cases.check_admin_session import CheckAdminSessionCase

from fastapi import Depends

from app.core.log.loguru_service import get_logger_service
from app.api.security.hashing.bcrypt_service import get_hasher_service
from app.api.security.jwt.jwt_service import get_jwt_repo
from app.api.dependencies.user.repo import get_user_repo

# dependencies
def get_register_user_case(
        user_repo = Depends(get_user_repo),
        hasher_repo = Depends(get_hasher_service),
        logger_service= Depends(get_logger_service, use_cache=True)
) -> RegisterUserCase:
    return RegisterUserCase(
        repo=user_repo,
        hasher=hasher_repo,
        logger=logger_service
    )

def get_login_user_case(
        user_repo = Depends(get_user_repo), 
        hasher_repo = Depends(get_hasher_service),
        logger_repo= Depends(get_logger_service, use_cache=True),
        jwt_repo = Depends(get_jwt_repo)
) -> LoginUserCase:
    return LoginUserCase(
        repo=user_repo,
        hasher=hasher_repo,
        logger=logger_repo,
        jwt=jwt_repo
    )

def get_logout_user_case(
        user_repo = Depends(get_user_repo), 
        jwt_repo = Depends(get_jwt_repo)
) -> LogoutUserCase:
    return LogoutUserCase(
        repo=user_repo,
        jwt=jwt_repo
    )

def get_check_user_session_case(
        user_repo = Depends(get_user_repo), 
        jwt_repo = Depends(get_jwt_repo),
        logger_repo= Depends(get_logger_service, use_cache=True)
) -> CheckUserSessionCase:
    return CheckUserSessionCase(
        repo=user_repo,
        jwt=jwt_repo,
        logger=logger_repo
    )

def get_check_admin_session_case(
    user_repo = Depends(get_user_repo), 
    jwt_repo = Depends(get_jwt_repo),
    logger_repo= Depends(get_logger_service, use_cache=True)
) -> CheckAdminSessionCase:
    return CheckAdminSessionCase(user_repo, jwt_repo, logger_repo)