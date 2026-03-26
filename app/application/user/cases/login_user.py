from app.domain.user.dto import LoginUserCommand
from app.application.user.service import UserService

class LoginUserCase:
    def __init__(
            self,
            user_service: UserService
            ):
        self._user_service = user_service


    async def execute(
            self,
            command: LoginUserCommand
    ) -> dict[str, str]:
        return await self._user_service.login_user(command)
        
        


