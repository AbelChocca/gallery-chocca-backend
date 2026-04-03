from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.api.security.hashing.protocole import HashProtocole
from app.infra.db.exceptions import DatabaseException
from app.api.security.exceptions import AuthException
from app.core.exceptions import ValidationError, ValueNotFound
from app.domain.user.entity import User
from app.domain.user.dto import RegisterUserCommand, LoginUserCommand
from app.shared.services.pagination.pagination_service import PaginationService
from app.api.security.jwt.protocole import JWTProtocole
from app.core.settings.pydantic_settings import Settings
from app.domain.user.constraints import USER_EXCEPTIONS_TRANSLATIONS

class UserService:
    def __init__(
            self,
            user_repo: PostgresUserRepository,
            favorite_repo: PostgresFavoritesRepository,
            hasher_service: HashProtocole,
            jwt_service: JWTProtocole,
            pagination_service: PaginationService,
            settings: Settings
        ):
        self._user_repo = user_repo
        self._favorite_repo = favorite_repo
        self._hasher_service = hasher_service
        self._jwt_service = jwt_service
        self._pagination_service = pagination_service
        self._settings = settings

    def logout_user(self) -> dict:
        """
        Handles user logout by verifying the presence of a valid token
        and removing JWT cookies from the response.
        """
        try:
            self._jwt_service.get_token_from_cookies()

        except ValueNotFound:
            ...

        self._jwt_service.delete_cookie("session_token")
        self._jwt_service.delete_cookie("refresh_token")

        return {"message": "Logout was successful!"}
    
    async def count_users(self, related_name: str | None = None) -> int:
        total_count: int = await self._user_repo.count_all(related_name)

        return total_count

    async def get_users(
        self, 
        *,
        related_name: str | None = None,
        page: int = 1,
        limit: int = 20
    ) -> dict:
        offset: int = self._pagination_service.get_offset(page, limit)
        users = await self._user_repo.get_all(
            related_name=related_name,
            offset=offset,
            limit=limit
        )
        total_count: int = await self.count_users(related_name)

        total_pages = self._pagination_service.get_total_pages(total_count, limit)
        current_page = self._pagination_service.get_current_page(offset, limit)

        return {
            "users": [
                user.to_dict
                for user in users
            ],
            "pagination": {
                "total_pages": total_pages,
                "current_page": current_page
            },
            "total_items": total_count
        }
    
    async def get_user_by_id(self, user_id: int) -> dict:
        user = await self._user_repo.get_by_id(user_id)

        return user.to_dict

    async def login_user(self, command: LoginUserCommand) -> dict[str, str]:
        user = await self._user_repo.get_by_email(command.email)

        if not self._hasher_service.verify(command.password, user.hashed_password):
            raise AuthException(
                "Password incorrect, retry.",
                {
                    "event": "login_user"
                }
            )
        
        payload: dict = {'sub': command.email, 'role': user.role}
        
        a_token = self._jwt_service.generate_token(payload)
        r_token = self._jwt_service.generate_token(payload, True)

        self._jwt_service.set_cookie(
            key="session_token",
            token=a_token,
            expires=self._settings.ACCESS_TOKEN_EXPIRES_SECONDS
        )
        self._jwt_service.set_cookie(
            key="refresh_token",
            token=r_token,
            expires=self._settings.REFRESH_TOKEN_EXPIRES_SECONDS
        )
        return {"message": "Login successful"}
    
    async def register_user(
        self, 
        command: RegisterUserCommand,
        anon_session_id: int | None = None
    ) -> dict:
        try:
            hashed_password = self._hasher_service.hash(command.password)

            user = User(
                name=command.name,
                email=command.email,
                hashed_password=hashed_password
            )

            res = await self._user_repo.save(user)

            if anon_session_id is not None:
                await self._favorite_repo.set_anon_session_favorites_to_user_favorites(anon_session_id, res.id)

            return {
                "id": res.id,
                "nombre": res.name,
                "email": res.email,
                "role": res.role
            }
        except DatabaseException as db:
            if db.context.get("db_error_code") == "integrity_error":

                constraint = db.context.get("original_error").lower()

                for key, (field, code) in USER_EXCEPTIONS_TRANSLATIONS.items():
                    if key.lower() in constraint:
                        raise ValidationError(
                            field,
                            {
                                "app_error_code": code,
                                "event": "register_user"
                            }
                        )
            raise db
        
    async def count_users_by_active_session(self) -> dict:
        results = await self._user_repo.count_users_by_active_session()
        user_counts = { "active" if is_active else "inactive": count for is_active, count in results }

        return user_counts
    
    async def count_users_per_role(self) -> list[dict]:
        total_users_per_role = await self._user_repo.count_user_per_role()

        return [
            {
                "total": total,
                "role": role
            }
            for (role, total) in total_users_per_role
        ]

    async def get_last_n_users(self, n: int) -> list[dict]:
        users = await self._user_repo.get_last_n_users(n)

        return [
            user.to_dict
            for user in users
        ]