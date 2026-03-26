from app.application.user.service import UserService
from app.infra.db.unit_of_work import UnitOfWork

from fastapi import Depends
from app.api.dependencies.uow import get_uow
from app.api.security.hashing.bcrypt_service import get_hasher_service
from app.shared.services.pagination.pagination_service import get_pagination_service
from app.api.security.jwt.jwt_service import get_jwt_repo
from app.core.settings.pydantic_settings import get_settings

def get_user_service(
        uow: UnitOfWork = Depends(get_uow), 
        hasher_service = Depends(get_hasher_service),
        jwt_service = Depends(get_jwt_repo),
        settings = Depends(get_settings),
        pagination_service = Depends(get_pagination_service)
    ) -> UserService:
    return UserService(
        user_repo=uow.users,
        favorite_repo=uow.favorites,
        hasher_service=hasher_service,
        jwt_service=jwt_service,
        pagination_service=pagination_service,
        settings=settings
    )