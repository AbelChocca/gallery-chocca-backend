from app.application.media.service import MediaService
from app.domain.slide.slide_dto import PublishSlideCommand
from app.infra.saga_service import SagaService
from app.application.slides.service import SlideService
from app.core.app_exception import AppException

from typing import BinaryIO

class PublishSlideCase:
    def __init__(
            self,
            slide_service: SlideService,
            saga_service: SagaService,
            media_service: MediaService
            ):
        self._slide_service: SlideService = slide_service
        self._saga_service: SagaService = saga_service
        self._media_service: MediaService = media_service

    async def exec(self, image_file: BinaryIO, command: PublishSlideCommand) -> None:
        try:
            return await self._slide_service.create_slide(
                command,
                image_file,
                saga_service=self._saga_service,
                action_func=self._media_service.upload_image,
                compensation_func=self._media_service.move_image_to_trash
            )
            
        except AppException as ae:
            await self._saga_service.compensate_all()

            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae