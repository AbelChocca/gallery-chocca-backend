from app.application.slides.cases.delete_slide import DeleteSlideCase
from app.application.slides.cases.publish_slide import PublishSlideCase
from app.application.slides.cases.update_slide import UpdateSlideCase
from app.application.slides.cases.get_slides import GetSlidesCase
from app.modules.slide.domain.slide_repository import SlideRepository

from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository

from app.api.dependencies.slides.repo import get_slide_repo
from app.api.dependencies.cloudinary.repo import get_cloudinary_repo

from app.core.log.logger_repository import LoggerRepository
from app.core.log.loguru_logger_repository import get_logger_repo

from fastapi import Depends

def get_slides_case(repo: SlideRepository = Depends(get_slide_repo)) -> GetSlidesCase:
    return GetSlidesCase(repo)

def get_delete_slide_case(repo: SlideRepository = Depends(get_slide_repo), image_repo: CloudinaryRepository = Depends(get_cloudinary_repo)) -> DeleteSlideCase:
    return DeleteSlideCase(repo=repo, image_repo=image_repo)

def get_publish_slide_case(
        repo: SlideRepository = Depends(get_slide_repo),
        image_repo: CloudinaryRepository = Depends(get_cloudinary_repo)
        ) -> PublishSlideCase:
    return PublishSlideCase(repo=repo, image_repo=image_repo)

def get_update_slide_case(
        repo: SlideRepository = Depends(get_slide_repo),
        image_repo: CloudinaryRepository = Depends(get_cloudinary_repo),
        logger: LoggerRepository = Depends(get_logger_repo)
        ) -> UpdateSlideCase:
    return UpdateSlideCase(repo=repo, image_repo=image_repo, logger=logger)
