from app.application.media.service import MediaService
from app.core.app_exception import AppException
from app.infra.saga_service import SagaService

class DeleteImageCase:
    def __init__(
            self,
            media_service: MediaService,
            saga_service: SagaService
            ):
        self.media_service = media_service
        self._saga_service = saga_service

    async def execute(self, public_id: str) -> dict[str, str]:
        try:
            self._saga_service.add_step(
                action=self.media_service.move_image_to_trash,
                action_name="move_image_to_trash",
                action_kwargs={
                    "public_id": public_id
                },
                compensation=self.media_service.recover_image_from_trash,
                compensation_name="recover_image_from_trash",
                compensation_kwargs={
                    "public_id": public_id
                }
            )
            await self._saga_service.execute_last()
            
            return {"meesage": "The Image was deleted successfully"}
        except AppException as ae:
            await self._saga_service.compensate_all()

            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae