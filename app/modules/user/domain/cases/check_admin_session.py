from app.core.security.jwt.abstract_repo import JWTRepository
from app.modules.user.domain.repository_user import UserRepository
from app.core.log.repository_logger import LoggerRepository
from app.modules.user.domain.user import User

from app.shared.exceptions.domain.user_exception import UserNotFoundException
from app.shared.exceptions.domain.jwt_exception import TokenNotFound, ForceLoginError, ForbiddenException
from app.shared.exceptions.infra.infraestructure_exception import JWTException


class CheckAdminSessionCase:
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
            user_role = payload.get("role")
            user_email = payload.get("sub")
            if user_role != "admin":
                self.logger.warning(f"Unknow user with email: {user_email} was tried to access admin route.")
                raise ForbiddenException()

            admin = await self.repo.get_by_email(user_email)

            if admin.role != "admin":
                raise ForbiddenException("User role in DB is not admin.")

            return admin
        except (TokenNotFound, JWTException, UserNotFoundException, ForceLoginError) as e:
            self.logger.warning(f"Admin session check failed: {str(e)}")
            raise e
        