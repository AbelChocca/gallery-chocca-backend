from app.application.media.service import MediaService
from app.infra.media.cloudinary_service import CloudinaryService, get_cloudinary_service
from app.infra.db.unit_of_work import UnitOfWork
from app.infra.async_utils import AsyncService, get_async_service

from app.api.dependencies.uow import get_uow

from fastapi import Depends

def get_media_service(
        cloudinary_service: CloudinaryService = Depends(get_cloudinary_service),
        uow: UnitOfWork = Depends(get_uow),
        async_service: AsyncService = Depends(get_async_service)
        ) -> MediaService:
    return MediaService(
        image_repo=uow.images,
        cloudinary_service=cloudinary_service,
        async_service=async_service
    )