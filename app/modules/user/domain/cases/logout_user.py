from app.modules.user.domain.repository_user import UserRepository
from app.core.security.jwt.abstract_repo import JWTRepository

from app.shared.exceptions.domain.jwt_exception import TokenNotFound
from app.shared.exceptions.domain.domain_exception import DomainException

from typing import Dict

class LogoutUserCase:
    def __init__(
            self,
            repo: UserRepository,
            jwt: JWTRepository
            ):
        self.repo = repo
        self.jwt = jwt


    async def execute(
            self
    ) -> Dict[str, str]:
        """
        Handles user logout by verifying the presence of a valid token
        and removing JWT cookies from the response.
        """
        try:
            payload_verify = self.jwt.get_token_from_cookies()

        except TokenNotFound:
            auth_token = None

        self.jwt.delete_refresh_cookie()
        self.jwt.delete_session_cookie()

        return {"message": "Logout was successful!"}
        