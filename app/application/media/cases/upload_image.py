from app.application.media.service import MediaService
from app.domain.media.media_dto import MediaImageDTO
from app.core.app_exception import AppException
from app.infra.saga_service import SagaService

from typing import BinaryIO

class UploadImageCase:
    def __init__(
            self,
            media_service: MediaService,
            saga_service: SagaService
            ):
        self.media_service = media_service
        self._saga_service = saga_service

    async def execute(self, file: BinaryIO, folder: str) -> MediaImageDTO:
        try:
            self._saga_service.add_step(
                action=self.media_service.upload_image,
                action_name="upload_image",
                action_kwargs={
                    "image_resource": file,
                    "folder": folder
                }
            )
            res: MediaImageDTO = await self._saga_service.execute_last()
            self._saga_service.set_last_step_compensation(
                compesation=self.media_service.move_image_to_trash,
                compensation_name="move_image_to_trash",
                compensation_kwargs={
                    "public_id": res.public_id
                }
            )
            
        except AppException as ae:
            await self._saga_service.compensate_all()

            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae