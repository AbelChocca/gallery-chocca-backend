from app.features.user.service import UserService
from app.infra.db.uow.unit_of_work import UnitOfWork

from fastapi import Depends
from app.infra.db.uow.dependency import get_uow
from app.shared.pagination.pagination_service import get_pagination_service
from app.core.settings.pydantic_settings import get_settings

def get_user_service(
        uow: UnitOfWork = Depends(get_uow),
        settings = Depends(get_settings),
        pagination_service = Depends(get_pagination_service)
    ) -> UserService:
    return UserService(
        user_repo=uow.users,
        favorite_repo=uow.favorites,
        pagination_service=pagination_service,
        settings=settings
    )