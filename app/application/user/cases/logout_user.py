from app.modules.user.domain.repository_user import UserRepository
from app.api.security.jwt.jwt_repository import JWTRepository

from app.api.security.jwt.jwt_exception import TokenNotFound

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
        