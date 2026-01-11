from app.api.security.jwt.protocole import JWTProtocole
from app.core.log.protocole import LoggerProtocol
from app.domain.user.dto import ReadUserDTO
from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository

from app.api.security.jwt.jwt_exception import ForbiddenException


class CheckAdminSessionCase:
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
        user_role = payload.get("role")
        user_email = payload.get("sub")
        if user_role != "admin":
            self.logger.warning(f"Unknow user with email: {user_email} was tried to access admin route.")
            raise ForbiddenException()

        admin = await self.repo.get_by_email(user_email)

        if admin.role != "admin":
            raise ForbiddenException("User role in DB is not admin.")

        return ReadUserDTO(
            id=admin.id,
            nombre=admin.name,
            email=admin.email,
            role=admin.role
        )
        