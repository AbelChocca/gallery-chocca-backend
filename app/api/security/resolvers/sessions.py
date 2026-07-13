from app.api.security.jwt.jwt_service import JWTService, get_jwt_service
# Ocassionally
from app.infra.db.repositories.sqlalchemy_user_repository import PostgresUserRepository
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.infra.db.uow.dependency import get_uow
from fastapi import Depends

from app.api.security.exceptions import SecurityException
from app.core.exceptions import ValueNotFound
from app.features.auth.schema import ReadSessionSchema
from app.features.user.user_schema import ReadUserSchema
from app.core.authorization.role_permissions import ROLE_PERMISSIONS

class SecuritySessions:
    def __init__(
            self,
            jwt: JWTService,
            user_repo: PostgresUserRepository
            ):
        self.jwt = jwt
        self.user_repo = user_repo

    async def _get_user(self):
        payload = self.jwt.get_token_from_cookies()

        if payload is None:
            return None
        
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

    async def get_user_info(self) -> ReadUserSchema:        
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
        
        return ReadUserSchema(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            role=user.role
        )
    
    async def get_user_session(self) -> ReadSessionSchema | None:       
        user = await self._get_user()
        if user is None:
            return None
        
        if not user.is_active:
            raise SecurityException(
                "Account's not longer active.",
                {
                    "service": "sessions/security",
                    "event": "get_user_session"
                }
            )
        
        return ReadSessionSchema(
            id=user.id,
            role=user.role,
            permissions=ROLE_PERMISSIONS[user.role]
        )

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
    
def get_auth_sessions(jwt: JWTService = Depends(get_jwt_service), uow: UnitOfWork = Depends(get_uow)) -> SecuritySessions:
    return SecuritySessions(jwt=jwt, user_repo=uow.users)

async def get_user_info(auth: SecuritySessions = Depends(get_auth_sessions)) -> ReadUserSchema:
    return await auth.get_user_info()

async def get_user_id(auth: SecuritySessions = Depends(get_auth_sessions)) -> int | None:
    return await auth.get_user_id()

async def get_user_session(
    auth: SecuritySessions = Depends(get_auth_sessions)
) -> ReadSessionSchema | None:
    return await auth.get_user_session()