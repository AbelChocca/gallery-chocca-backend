from app.core.security.jwt.abstract_repo import JWTRepository
from app.modules.user.domain.repository_user import UserRepository
from app.core.log.repository_logger import LoggerRepository
from app.modules.user.domain.user import User

from app.shared.exceptions.domain.user_exception import UserNotFoundException
from app.shared.exceptions.domain.jwt_exception import TokenNotFound, ForceLoginError
from app.shared.exceptions.infra.infraestructure_exception import JWTException


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
    ) -> User:
        try:
            payload = self.jwt.get_token_from_cookies()

            user = await self.repo.get_by_email(payload.get('sub'))

            return user
        except (TokenNotFound, JWTException, UserNotFoundException, ForceLoginError) as e:
            self.logger.warning(f"User session check failed: {str(e)}")
            raise e
        