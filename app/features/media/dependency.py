from app.features.media.service import MediaService
from app.infra.storage.cloudinary_service import CloudinaryService, get_cloudinary_service
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.infra.async_utils import AsyncService, get_async_service
from app.infra.saga.saga_service import SagaService,get_saga_service

from app.infra.db.uow.dependency import get_uow

from fastapi import Depends

def get_media_service(
        cloudinary_service: CloudinaryService = Depends(get_cloudinary_service),
        uow: UnitOfWork = Depends(get_uow),
        async_service: AsyncService = Depends(get_async_service),
        saga_service: SagaService = Depends(get_saga_service)
        ) -> MediaService:
    return MediaService(
        image_repo=uow.images,
        storage_service=cloudinary_service,
        async_service=async_service,
        saga_service=saga_service
    )