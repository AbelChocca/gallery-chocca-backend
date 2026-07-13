from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.infra.db.repositories.sqlalchemy_user_repository import PostgresUserRepository
from app.infra.db.repositories.sqlalchemy_cart_repository import CartRepository
from app.infra.db.exceptions import DatabaseException
from app.core.exceptions import ValidationError, InvalidOperation, ValueNotFound
from app.features.user.entity import User
from app.shared.pagination.pagination_service import PaginationService
from app.core.settings.pydantic_settings import Settings
from app.features.user.constraints import USER_EXCEPTIONS_TRANSLATIONS
from app.features.user.types import UserRole
from app.features.user.dto import CountUsersPerRoleDTO

class UserService:
    def __init__(
            self,
            user_repo: PostgresUserRepository,
            favorite_repo: PostgresFavoritesRepository,
            cart_repo: CartRepository,
            pagination_service: PaginationService,
            settings: Settings
        ):
        self._user_repo = user_repo
        self._favorite_repo = favorite_repo
        self._cart_repository = cart_repo
        self._pagination_service = pagination_service
        self._settings = settings

    async def create_user(
            self,
            name: str,
            email: str,
            hashed_password: str,
            anon_session_id: int | None = None
    ) -> User:
        try:
            user = User(
                    name=name,
                    email=email,
                    hashed_password=hashed_password
                )

            res = await self._user_repo.save(user)

            if anon_session_id is not None:
                await self._favorite_repo.set_anon_session_favorites_to_user_favorites(anon_session_id, res.id)

                await self._cart_repository.migrate_session_cart_to_user(
                    session_id=anon_session_id,
                    user_id=res.id
                )

            return res
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
        
    async def update_role_by_user_id(
        self,
        user_id: int,
        role: UserRole
    ) -> None:
        user = await self._user_repo.get_by_id(user_id)

        if not user:
            raise ValueNotFound(
                "Cannot found the user to update role.",
                {
                    "user_id": user_id,
                    "service": "user",
                    "event": "update_role_by_user_id",
                    "current_role": user.role,
                    "requested_role": role,
                }
            )

        if not user.is_active:
            raise InvalidOperation(
                "Cannot change the role of an inactive user.",
                {
                    "service": "user",
                    "event": "update_role_by_user_id",
                    "user_id": user_id,
                    "current_role": user.role,
                    "requested_role": role,
                }
            )

        await self._user_repo.update_role_by_user_id(
            user_id=user_id,
            role=role,
        )

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
        total_count: int = await self._count_users(related_name)

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
    
    async def get_user_by_email(self, email: str):
        user = await self._user_repo.get_by_email(email)

        return user
        
    async def _count_users_by_active_session(
        self
    ) -> dict:

        results = await self._user_repo.count_users_by_active_session()

        counts = {
            "active": 0,
            "inactive": 0
        }

        for is_active, count in results:
            key = "active" if is_active else "inactive"
            counts[key] = count

        return counts
    
    async def _count_users_per_role(self) -> list[CountUsersPerRoleDTO]:
        total_users_per_role = await self._user_repo.count_user_per_role()

        res: list[CountUsersPerRoleDTO] = [
            CountUsersPerRoleDTO(
                total=total,
                role=role
            )
            for (role, total) in total_users_per_role
        ]

        return res

    async def _get_last_n_users(self, n: int) -> list[dict]:
        users = await self._user_repo.get_last_n_users(n)

        return [
            user.to_dict
            for user in users
        ]
    
    async def _count_users(self, related_name: str | None = None) -> int:
        total_count: int = await self._user_repo.count_all(related_name)

        return total_count