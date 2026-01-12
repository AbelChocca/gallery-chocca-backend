from app.application.slides.cases.delete_slide import DeleteSlideCase
from app.application.slides.cases.publish_slide import PublishSlideCase
from app.application.slides.cases.update_slide import UpdateSlideCase
from app.application.slides.cases.get_slides import GetSlidesCase
from app.infra.db.repositories.sqlmodel_slide_repository import PostgresSlideRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository

from app.infra.media.cloudinary_service import CloudinaryService

from app.api.dependencies.slides.repo import get_slide_repo
from app.api.dependencies.media.service import get_media_service
from app.api.dependencies.media.repo import get_image_repo

from app.core.log.protocole import LoggerProtocol
from app.core.log.loguru_service import get_logger_service

from fastapi import Depends

def get_slides_case(
        slide_repo: PostgresSlideRepository = Depends(get_slide_repo),
        image_repo: PostgresImageRepository = Depends(get_image_repo)
        ) -> GetSlidesCase:
    return GetSlidesCase(
        slide_repo=slide_repo,
        image_repo=image_repo
    )

def get_delete_slide_case(
        slide_repo: PostgresSlideRepository = Depends(get_slide_repo), 
        image_repo: PostgresImageRepository = Depends(get_image_repo),
        media_service: CloudinaryService = Depends(get_media_service)
        ) -> DeleteSlideCase:
    return DeleteSlideCase(
        slide_repo=slide_repo,
        image_repo=image_repo,
        media_service=media_service
        )

def get_publish_slide_case(
        slide_repo: PostgresSlideRepository = Depends(get_slide_repo),
        image_repo: PostgresSlideRepository = Depends(get_image_repo),
        media_service: CloudinaryService = Depends(get_media_service)
        ) -> PublishSlideCase:
    return PublishSlideCase(
        slide_repo=slide_repo,
        image_repo=image_repo,
        media_service=media_service
        )

def get_update_slide_case(
        slide_repo: PostgresSlideRepository = Depends(get_slide_repo),
        image_repo: PostgresImageRepository = Depends(get_image_repo),
        media_service:CloudinaryService = Depends(get_media_service),
        logger: LoggerProtocol = Depends(get_logger_service)
        ) -> UpdateSlideCase:
    return UpdateSlideCase(
        slide_repo=slide_repo,
        image_repo=image_repo, 
        media_service=media_service,
        logger=logger
        )
