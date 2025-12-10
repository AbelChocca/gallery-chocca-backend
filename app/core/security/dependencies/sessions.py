from app.core.security.jwt.abstract_repo import JWTRepository
from app.core.security.jwt.jwt_repository import get_jwt_repo
from app.shared.exceptions.domain.jwt_exception import Unauthorized, ForbiddenException

# Ocassionally
from app.modules.user.domain.repository_user import UserRepository
from app.modules.user.interface.dependencies.repo import get_user_repo
from fastapi import Depends


class SecuritySessions:
    def __init__(
            self,
            jwt: JWTRepository,
            user_repo: UserRepository
            ):
        self.jwt = jwt
        self.user_repo = user_repo

    async def get_user_session(self) -> None:
        payload = self.jwt.get_token_from_cookies()

        if not payload:
            raise Unauthorized()
        
        user = await self.user_repo.get_by_email(payload.get("sub"))
        if not user:
            raise Unauthorized()

    async def get_admin(self) ->  None:
        payload = self.jwt.get_token_from_cookies()

        if not payload:
            raise Unauthorized()
        
        admin = await self.user_repo.get_by_email(payload.get("sub"))
        if not admin:
            raise Unauthorized()
        
        if admin.role != "admin":
            raise ForbiddenException()
    
def get_auth_sessions(jwt: JWTRepository = Depends(get_jwt_repo), user_repo: UserRepository = Depends(get_user_repo)) -> SecuritySessions:
    return SecuritySessions(jwt=jwt, user_repo=user_repo)