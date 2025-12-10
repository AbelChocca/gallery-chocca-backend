from app.shared.dto.user_dto import LoginUserDTO
from app.modules.user.domain.repository_user import UserRepository
from app.core.security.bcrypt.repository_passwordhash import PasswordHashRepository
from app.core.log.repository_logger import LoggerRepository
from app.core.security.jwt.abstract_repo import JWTRepository
from app.shared.exceptions.infra.infraestructure_exception import JWTException
from app.shared.exceptions.domain.domain_exception import DomainException
from app.shared.exceptions.domain.user_exception import UserNotFoundException, InvalidPassword

from typing import Dict
from datetime import timedelta

class LoginUserCase:
    def __init__(
            self,
            repo: UserRepository,
            hasher: PasswordHashRepository,
            logger: LoggerRepository,
            jwt: JWTRepository
            ):
        self.repo = repo
        self.hasher = hasher
        self.logger = logger
        self.jwt = jwt


    async def execute(
            self,
            dto: LoginUserDTO
    ) -> Dict[str, str]:
        try:
            user = await self.repo.get_by_email(dto.email)

            if not self.hasher.verify(dto.password, user.hashed_password):
                self.logger.warning(f"Password incorrect, retry.")
                raise InvalidPassword()
            
            a_token = self.jwt.generate_token({'sub': dto.email, 'role': user.role})
            r_token = self.jwt.generate_token({'sub': dto.email, 'role': user.role}, True)

            self.jwt.set_jwt_cookie(a_token)
            self.jwt.set_refresh_token_cookie(r_token)
            return {"message": "Login successful"}
        except UserNotFoundException as e:
            raise DomainException("Cannot found user.") from e
        except JWTException as e:
            self.logger.error(f"JWT Internal's error: {str(e)}")
            raise e
        
        


