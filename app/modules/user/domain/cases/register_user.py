from app.shared.dto.user_dto import RegisterUserDTO
from app.modules.user.domain.repository_user import UserRepository
from app.core.security.bcrypt.repository_passwordhash import PasswordHashRepository
from app.core.log.repository_logger import LoggerRepository
from app.modules.user.domain.user import User

from app.shared.exceptions.domain.user_exception import (
    UserNotFoundException,
    EmailTooShortException,
    InvalidEmailFormatException,
    PasswordTooShortException
    )
from app.shared.exceptions.infra.infraestructure_exception import DatabaseException

class RegisterUserCase:
    def __init__(
            self, 
            repo: UserRepository,
            hasher: PasswordHashRepository,
            logger: LoggerRepository
            ):
        self.repo = repo
        self.hasher = hasher
        self.logger = logger

    async def exec(
            self,
            dto: RegisterUserDTO
            ) -> User:
        hashed_password = self.hasher.hash(dto.password)

        try:
            user = User(
                name=dto.nombre,
                email=dto.email,
                hashed_password=hashed_password,
                role=dto.role
            )

            res = await self.repo.save(user)
            return res
        except (EmailTooShortException, InvalidEmailFormatException, PasswordTooShortException, UserNotFoundException) as e:
            self.logger.error(f"Domain's service error: {str(e)}")
            raise e
        
        except DatabaseException as e:
            self.logger.error(f"Internal's server error: {str(e)}")
            raise e
        
