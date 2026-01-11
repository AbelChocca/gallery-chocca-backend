from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.api.security.jwt.protocole import JWTProtocole

from app.api.security.jwt.jwt_exception import TokenNotFound

from typing import Dict

class LogoutUserCase:
    def __init__(
            self,
            repo: PostgresUserRepository,
            jwt: JWTProtocole
            ):
        self._repo = repo
        self._jwt = jwt


    async def execute(
            self
    ) -> Dict[str, str]:
        """
        Handles user logout by verifying the presence of a valid token
        and removing JWT cookies from the response.
        """
        try:
            payload_verify = self._jwt.get_token_from_cookies()

        except TokenNotFound:
            auth_token = None

        self._jwt.delete_cookie("session_cookie")
        self._jwt.delete_cookie("refresh_cookie")

        return {"message": "Logout was successful!"}
        