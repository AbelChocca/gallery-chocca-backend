from app.modules.slide.interface.dependencies.repo import get_slide_repo
from app.modules.slide.domain.cases.delete_slide import DeleteSlideCase
from app.modules.slide.domain.cases.publish_slide import PublishSlideCase
from app.modules.slide.domain.cases.update_slide import UpdateSlideCase
from app.modules.slide.domain.cases.get_slides import GetSlidesCase
from app.modules.slide.domain.slide_repository import SlideRepository

from fastapi import Depends

def get_slides_case(repo: SlideRepository = Depends(get_slide_repo)) -> GetSlidesCase:
    return GetSlidesCase(repo)

def get_delete_slide_case(repo: SlideRepository = Depends(get_slide_repo)) -> DeleteSlideCase:
    return DeleteSlideCase(repo)

def get_publish_slide_case(repo: SlideRepository = Depends(get_slide_repo)) -> PublishSlideCase:
    return PublishSlideCase(repo)

def get_update_slide_case(repo: SlideRepository = Depends(get_slide_repo)) -> UpdateSlideCase:
    return UpdateSlideCase(repo)
