from app.application.user.commands import LoginUserCommand
from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.api.security.hashing.hash_repository import HashRepository
from app.core.log.protocole import LoggerProtocol
from app.core.settings.pydantic_settings import Settings
from app.api.security.jwt.protocole import JWTProtocole
from app.domain.user.user_exception import InvalidPassword

from typing import Dict, Any

class LoginUserCase:
    def __init__(
            self,
            repo: PostgresUserRepository,
            hasher: HashRepository,
            logger: LoggerProtocol,
            jwt: JWTProtocole,
            settings: Settings
            ):
        self._repo = repo
        self._hasher = hasher
        self._logger = logger
        self._jwt = jwt
        self._settings = settings


    async def execute(
            self,
            command: LoginUserCommand
    ) -> Dict[str, str]:
        user = await self._repo.get_by_email(command.email)

        if not self._hasher.verify(command.password, user.hashed_password):
            self._logger.warning(f"Password incorrect, retry.")
            raise InvalidPassword()
        
        payload: Dict[str, Any] = {'sub': command.email, 'role': user.role}
        
        a_token = self._jwt.generate_token(payload)
        r_token = self._jwt.generate_token(payload, True)

        self._jwt.set_cookie(
            key="session_cookie",
            token=a_token,
            expires=self._settings.ACCESS_TOKEN_EXPIRES_SECONDS
        )
        self._jwt.set_cookie(
            key="refresh_cookie",
            token=r_token,
            expires=self._settings.REFRESH_TOKEN_EXPIRES_SECONDS
        )
        return {"message": "Login successful"}
        
        


