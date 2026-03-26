from app.application.media.service import MediaService
from app.infra.saga_service import SagaService
from app.application.products.service import ProductService

from app.domain.product.dto.product_dto import CreateProductResponse
from app.domain.product.dto.product_dto import PublishProductCommand
from app.core.app_exception import AppException

from typing import List, BinaryIO

class CreateProductUseCase:
    def __init__(
            self, 
            product_service: ProductService,
            media_service: MediaService,
            saga_service: SagaService
            ):
        self._product_service = product_service
        self._media_service = media_service
        self._saga_service = saga_service
        

    async def execute(
            self, 
            images_file: List[BinaryIO],
            command: PublishProductCommand
            ) -> CreateProductResponse:
        self._product_service.validate_product_form(images_file, command)
        try:
            images_by_temp_key = await self._product_service.upload_images_by_temp_key(
                self._saga_service,
                images_file,
                command.temp_keys,
                self._media_service.upload_images_batch,
                self._media_service.move_images_to_trash
            )

            created_product = await self._product_service.create_product_with_variants(
                command,
                images_by_temp_key
            )
            return CreateProductResponse(created_product.id, created_product.slug)
        except AppException as ae:
            await self._saga_service.compensate_all()

            ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae