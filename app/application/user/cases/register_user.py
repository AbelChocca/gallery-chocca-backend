from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository

from app.api.security.hashing.hash_repository import HashRepository
from app.core.log.protocole import LoggerProtocol
from app.domain.user.entity import User
from app.domain.user.dto import ReadUserDTO
from app.application.user.commands import RegisterUserCommand


class RegisterUserCase:
    def __init__(
            self, 
            repo: PostgresUserRepository,
            hasher: HashRepository,
            logger: LoggerProtocol
            ):
        self._repo = repo
        self._hasher = hasher
        self._logger = logger

    async def exec(
            self,
            command: RegisterUserCommand
            ) -> ReadUserDTO:
        hashed_password = self._hasher.hash(command.password)

        user = User(
            name=command.nombre,
            email=command.email,
            hashed_password=hashed_password,
            role=command.role
        )

        res = await self._repo.save(user)
        return ReadUserDTO(
            id=res.id,
            nombre=res.name,
            email=res.email,
            role=res.role
        )
        
