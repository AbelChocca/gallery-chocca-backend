from app.application.media.service import MediaService
from app.infra.saga_service import SagaService
from app.application.slides.service import SlideService
from app.core.app_exception import AppException

from typing import Dict, Any

class DeleteSlideCase:
    def __init__(
            self,
            saga_service: SagaService,
            slide_service: SlideService,
            media_service: MediaService
            ):
        self._saga_service = saga_service
        self.media_service = media_service
        self._slide_service = slide_service


    async def execute(self, slide_id: int) -> Dict[str, Any] | None:
        try:
            await self._slide_service.delete_slide(
                slide_id,
                self._saga_service,
                action_func=self.media_service.move_image_to_trash,
                compensation_func=self.media_service.recover_image_from_trash
            )
            await self._saga_service.execute_all()

            return {"message": f"Slide with id: {slide_id} was deleted."}
        except AppException as ae:
            await self._saga_service.compensate_all()
            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae
            