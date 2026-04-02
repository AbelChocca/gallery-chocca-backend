from app.api.security.jwt.protocole import JWTProtocole
from app.api.security.jwt.jwt_service import get_jwt_repo
# Ocassionally
from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.infra.db.unit_of_work import UnitOfWork
from app.api.dependencies.uow import get_uow
from fastapi import Depends

from app.api.security.exceptions import AuthException, SecurityException
from app.core.exceptions import ValueNotFound


class SecuritySessions:
    def __init__(
            self,
            jwt: JWTProtocole,
            user_repo: PostgresUserRepository
            ):
        self.jwt = jwt
        self.user_repo = user_repo

    async def _get_user(self):
        payload = self.jwt.get_token_from_cookies()

        if not payload:
            raise AuthException(
                "Unathorized session.",
                {
                    "service": "sessions/security",
                    "event": "_get_user"
                }
            )
        
        email = payload.get("sub")
        if not email:
            raise ValueNotFound(
                "Email empty or not exists.",
                {
                    "service": "sessions/security",
                    "event": "_get_user"
                }
            )
        
        user = await self.user_repo.get_by_email(email)
        return user

    async def get_user_session(self) -> dict:        
        user = await self._get_user()
        if not user:
            raise ValueNotFound(
                "User not found",
                {
                    "service": "sessions/security",
                    "event": "get_user_session"
                }
            )
        
        if not user.is_active:
            raise SecurityException(
                "Account's not longer active.",
                {
                    "service": "sessions/security",
                    "event": "get_user_session"
                }
            )
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }

    async def get_admin(self) ->  dict:
        admin = await self._get_user()
        if not admin:
            raise ValueNotFound(
                "User not found",
                {
                    "service": "sessions/security",
                    "event": "get_user_session"
                }
            )
        
        if not admin.is_active:
            raise SecurityException(
                "Account's not longer active.",
                {
                    "service": "sessions/security",
                    "event": "get_user_session"
                }
            )
        
        if admin.role != "admin":
            raise SecurityException(
                "Account's not longer active.",
                {
                    "service": "sessions/security",
                    "event": "get_user_session",
                    "role": admin.role
                }
            )
        
        return {
            "id": admin.id,
            "name": admin.name,
            "email": admin.email,
            "role": admin.role,
            "is_active": admin.is_active
        }

    async def get_user_id(self) -> int | None:
        session_token = self.jwt.get_session_token_from_cookies_with_no_raises()
        if not session_token:
            return None

        payload = self.jwt.verify_token(session_token)
        if not payload:
            return None
        
        email = payload.get("sub")
        if not email:
            return None
        
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        return user.id
    
def get_auth_sessions(jwt: JWTProtocole = Depends(get_jwt_repo), uow: UnitOfWork = Depends(get_uow)) -> SecuritySessions:
    return SecuritySessions(jwt=jwt, user_repo=uow.users)

async def get_admin_session(auth: SecuritySessions = Depends(get_auth_sessions)) -> dict:
    return await auth.get_admin()

async def get_user_session(auth: SecuritySessions = Depends(get_auth_sessions)) -> dict:
    return await auth.get_user_session()

async def get_user_id(auth: SecuritySessions = Depends(get_auth_sessions)) -> int | None:
    return await auth.get_user_id()
