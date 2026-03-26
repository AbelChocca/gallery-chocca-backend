from app.application.user.service import UserService

class GetUserByIDCase:
    def __init__(
            self,
            user_service: UserService
            ):
        self._user_service = user_service

    async def execute(self, user_id: int) -> dict:
        return await self._user_service.get_user_by_id(user_id)