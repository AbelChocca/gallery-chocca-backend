from app.api.dependencies.media.service import get_media_service
from app.infra.media.cloudinary_service import CloudinaryService
from app.application.media.cases.upload_image import UploadImageCase
from app.application.media.cases.delete_image import DeleteImageCase
from app.infra.saga_service import SagaService, get_saga_service

from fastapi import Depends

def get_upload_image_case(
        media_service: CloudinaryService = Depends(get_media_service),
        saga_service: SagaService = Depends(get_saga_service)
        ) -> UploadImageCase:
    return UploadImageCase(media_service, saga_service)

def get_delete_image_case(media_service: CloudinaryService = Depends(get_media_service),
        saga_service: SagaService = Depends(get_saga_service)) -> DeleteImageCase:
    return DeleteImageCase(media_service, saga_service)