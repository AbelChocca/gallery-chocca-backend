from app.api.security.jwt.protocole import JWTProtocole
from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.core.log.protocole import LoggerProtocol
from app.domain.user.dto import ReadUserDTO

class CheckUserSessionCase:
    def __init__(
            self,
            repo: PostgresUserRepository,
            jwt: JWTProtocole,
            logger: LoggerProtocol
            ):
        self.jwt: JWTProtocole = jwt
        self.repo: PostgresUserRepository = repo
        self.logger: LoggerProtocol = logger


    async def execute(
            self
    ) -> ReadUserDTO:
        payload = self.jwt.get_token_from_cookies()

        user = await self.repo.get_by_email(payload.get('sub'))

        return ReadUserDTO(
            id=user.id,
            nombre=user.name,
            email=user.email,
            role=user.role
        )
        