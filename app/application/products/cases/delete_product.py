from app.application.products.service import ProductService
from app.application.media.service import MediaService
from app.infra.saga_service import SagaService
from app.core.app_exception import AppException

class DeleteProductCase:
    def __init__(
            self,
            product_service: ProductService,
            media_service: MediaService,
            saga_service: SagaService
            ):
        self.product_service: ProductService = product_service
        self.media_service: MediaService = media_service
        self._saga_service: SagaService = saga_service

    async def execute(
            self,
            product_id: int
    ) -> None:
        try:
            await self.product_service.delete_product(
                product_id,
                self._saga_service,
                action_func=self.media_service.move_images_to_trash,
                compesantion_func=self.media_service.recover_images_from_trash
            )

            await self._saga_service.execute_all()
        except AppException as ae:
            await self._saga_service.compensate_all()

            if self._saga_service.compensation_errors:
                ae.context["compensation_errors"] = self._saga_service.compensation_errors

            return ae