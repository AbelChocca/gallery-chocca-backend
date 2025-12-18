from app.application.user.commands import LoginUserCommand
from app.modules.user.domain.repository_user import UserRepository
from app.api.security.hashing.hash_repository import HashRepository
from app.core.log.logger_repository import LoggerRepository
from app.api.security.jwt.jwt_repository import JWTRepository
from app.shared.exceptions.infraestructure_exception import JWTException
from app.modules.user.domain.user_exception import InvalidPassword

from typing import Dict

class LoginUserCase:
    def __init__(
            self,
            repo: UserRepository,
            hasher: HashRepository,
            logger: LoggerRepository,
            jwt: JWTRepository
            ):
        self.repo = repo
        self.hasher = hasher
        self.logger = logger
        self.jwt = jwt


    async def execute(
            self,
            command: LoginUserCommand
    ) -> Dict[str, str]:
        try:
            user = await self.repo.get_by_email(command.email)

            if not self.hasher.verify(command.password, user.hashed_password):
                self.logger.warning(f"Password incorrect, retry.")
                raise InvalidPassword()
            
            a_token = self.jwt.generate_token({'sub': command.email, 'role': user.role})
            r_token = self.jwt.generate_token({'sub': command.email, 'role': user.role}, True)

            self.jwt.set_jwt_cookie(a_token)
            self.jwt.set_refresh_token_cookie(r_token)
            return {"message": "Login successful"}
        except JWTException as e:
            self.logger.error(f"JWT Internal's error: {str(e)}")
            raise e
        
        


