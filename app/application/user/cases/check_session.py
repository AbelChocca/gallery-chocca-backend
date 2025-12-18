from app.api.security.jwt.jwt_repository import JWTRepository
from app.modules.user.domain.repository_user import UserRepository
from app.core.log.logger_repository import LoggerRepository
from app.modules.user.domain.dto import ReadUserDTO

from app.modules.user.domain.user_exception import UserNotFoundException
from app.api.security.jwt.jwt_exception import TokenNotFound, ForceLoginError
from app.shared.exceptions.infraestructure_exception import JWTException


class CheckUserSessionCase:
    def __init__(
            self,
            repo: UserRepository,
            jwt: JWTRepository,
            logger: LoggerRepository
            ):
        self.jwt: JWTRepository = jwt
        self.repo: UserRepository = repo
        self.logger: LoggerRepository = logger


    async def execute(
            self
    ) -> ReadUserDTO:
        try:
            payload = self.jwt.get_token_from_cookies()

            user = await self.repo.get_by_email(payload.get('sub'))

            return ReadUserDTO(
                id=user.id,
                nombre=user.name,
                email=user.email,
                role=user.role
            )
        except (TokenNotFound, JWTException, UserNotFoundException, ForceLoginError) as e:
            self.logger.warning(f"User session check failed: {str(e)}")
            raise e
        