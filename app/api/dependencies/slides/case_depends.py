from app.application.slides.cases.delete_slide import DeleteSlideCase
from app.application.slides.cases.publish_slide import PublishSlideCase
from app.application.slides.cases.update_slide import UpdateSlideCase
from app.application.slides.cases.get_slides import GetSlidesCase
from app.application.slides.cases.update_orders import UpdateOrdersCase
from app.application.slides.service import SlideService
from app.application.media.service import MediaService

from app.api.dependencies.media.service import get_media_service
from app.api.dependencies.slides.service import get_slide_service
from app.infra.saga_service import SagaService, get_saga_service

from fastapi import Depends

def get_slides_case(
        slide_service: SlideService = Depends(get_slide_service)
        ) -> GetSlidesCase:
    return GetSlidesCase(slide_service)

def get_delete_slide_case(
        slide_service: SlideService = Depends(get_slide_service),
        media_service: MediaService = Depends(get_media_service),
        saga_service: SagaService = Depends(get_saga_service)
        ) -> DeleteSlideCase:
    return DeleteSlideCase(
        slide_service=slide_service,
        media_service=media_service,
        saga_service=saga_service
        )

def get_publish_slide_case(
        slide_service: SlideService = Depends(get_slide_service),
        media_service: MediaService = Depends(get_media_service),
        saga_service: SagaService = Depends(get_saga_service)
        ) -> PublishSlideCase:
    return PublishSlideCase(
        slide_service=slide_service,
        media_service=media_service,
        saga_service=saga_service
        )

def get_update_slide_case(
        slide_service: SlideService = Depends(get_slide_service),
        media_service: MediaService = Depends(get_media_service),
        saga_service: SagaService = Depends(get_saga_service)
        ) -> UpdateSlideCase:
    return UpdateSlideCase(
        slide_service=slide_service,
        media_service=media_service,
        saga_service=saga_service
        )

def get_update_slide_orders_case(
    slide_service: SlideService = Depends(get_slide_service),
) -> UpdateOrdersCase:
    return UpdateOrdersCase(slide_service)