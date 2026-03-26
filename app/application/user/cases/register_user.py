from app.domain.user.dto import RegisterUserCommand
from app.application.user.service import UserService

class RegisterUserCase:
    def __init__(
            self, 
            user_service: UserService
            ):
        self._user_service = user_service

    async def exec(
            self,
            command: RegisterUserCommand,
            anon_session_id: int | None = None
            ) -> dict:
        return await self._user_service.register_user(command, anon_session_id)
        
