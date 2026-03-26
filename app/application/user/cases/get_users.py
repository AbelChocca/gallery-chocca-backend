from app.application.user.service import UserService

class GetUsersCase:
    def __init__(
            self,
            *,
            user_service: UserService
            ):
        self._user_service = user_service

    async def execute(
            self, 
            *,
            related_name: str | None= None,
            page: int = 1,
            limit: int = 20
            ) -> dict:
        return await self._user_service.get_users(
            related_name=related_name,
            page=page,
            limit=limit
        )


