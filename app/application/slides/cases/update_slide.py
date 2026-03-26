from app.core.exceptions import ValidationError
from app.core.app_exception import AppException
from app.domain.slide.slide_dto import UpdateSlideCommand
from app.infra.saga_service import SagaService
from app.application.slides.service import SlideService
from app.domain.slide.slide_entity import SlideEntity

from app.application.media.service import MediaService

from typing import BinaryIO

class UpdateSlideCase:
    def __init__(
            self,
            slide_service: SlideService,
            media_service: MediaService,
            saga_service: SagaService
            ):
        self._slide_service = slide_service
        self.media_service = media_service
        self._saga_service = saga_service

    async def _delete_entities(self, command: UpdateSlideCommand, slide: SlideEntity) -> None:
        if command.delete_image and slide.has_image:
            slide.image = await self._slide_service.delete_image(
                slide.image_public_id,
                self._saga_service,
                action_func=self.media_service.move_image_to_trash,
                compensation_func=self.media_service.recover_image_from_trash
            )

    async def execute(
        self, 
        slide_id: int, 
        new_slide_command: UpdateSlideCommand,
        new_image_file: BinaryIO | None = None
    ) -> None:
        try:
            slide = await self._slide_service.get_by_id(slide_id)
            if not new_slide_command.delete_image and new_image_file and slide.has_image:
                raise ValidationError(
                    "Current slide's image need to be deleted before upload a new image for the same slide.",
                    {
                        "module": "slides",
                        "case": "update_slide_case",
                        "event": "case/execute",
                    }
                )
            
            await self._delete_entities(new_slide_command, slide)

            await self._slide_service.update_slide(
                slide,
                new_slide_command,
                new_image_file,
                self._saga_service,
                action_func=self.media_service.upload_image,
                compensation_func=self.media_service.move_image_to_trash
            )

            await self._saga_service.execute_all()
        except AppException as ae:
            await self._saga_service.compensate_all()

            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae
        finally:
            self._saga_service.reset()