from app.api.security.jwt.protocole import JWTProtocole
from app.api.security.jwt.jwt_service import get_jwt_repo
from app.api.security.jwt.jwt_exception import Unauthorized, ForbiddenException

# Ocassionally
from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.api.dependencies.user.repo import get_user_repo
from fastapi import Depends


class SecuritySessions:
    def __init__(
            self,
            jwt: JWTProtocole,
            user_repo: PostgresUserRepository
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
    
def get_auth_sessions(jwt: JWTProtocole = Depends(get_jwt_repo), user_repo: PostgresUserRepository = Depends(get_user_repo)) -> SecuritySessions:
    return SecuritySessions(jwt=jwt, user_repo=user_repo)


async def get_admin_session(auth: SecuritySessions = Depends(get_auth_sessions)) -> None:
    await auth.get_admin()

async def get_user_session(auth: SecuritySessions = Depends(get_auth_sessions)) -> None:
    await auth.get_user_session()