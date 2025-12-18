from app.modules.user.domain.repository_user import UserRepository
from app.api.security.hashing.hash_repository import HashRepository
from app.core.log.logger_repository import LoggerRepository
from app.modules.user.domain.user import User
from app.modules.user.domain.dto import ReadUserDTO
from app.application.user.commands import RegisterUserCommand

from app.modules.user.domain.user_exception import (
    UserNotFoundException,
    EmailTooShortException,
    InvalidEmailFormatException,
    PasswordTooShortException
    )
from app.shared.exceptions.infraestructure_exception import DatabaseException

class RegisterUserCase:
    def __init__(
            self, 
            repo: UserRepository,
            hasher: HashRepository,
            logger: LoggerRepository
            ):
        self.repo = repo
        self.hasher = hasher
        self.logger = logger

    async def exec(
            self,
            command: RegisterUserCommand
            ) -> ReadUserDTO:
        hashed_password = self.hasher.hash(command.password)

        try:
            user = User(
                name=command.nombre,
                email=command.email,
                hashed_password=hashed_password,
                role=command.role
            )

            res = await self.repo.save(user)
            return ReadUserDTO(
                id=res.id,
                nombre=res.name,
                email=res.email,
                role=res.role
            )
        except (EmailTooShortException, InvalidEmailFormatException, PasswordTooShortException, UserNotFoundException) as e:
            self.logger.error(f"Domain's service error: {str(e)}")
            raise e
        
        except DatabaseException as e:
            self.logger.error(f"Internal's server error: {str(e)}")
            raise e
        
