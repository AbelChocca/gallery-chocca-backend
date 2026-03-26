from app.application.media.service import MediaService
from app.domain.product.dto.product_dto import UpdateProductCommand
from app.infra.saga_service import SagaService
from app.application.products.service import ProductService
from app.core.app_exception import AppException
from app.core.exceptions import ValidationError

from typing import BinaryIO, List

class UpdateProductCase:
    def __init__(
            self,
            product_service: ProductService,
            saga_service: SagaService,
            media_service: MediaService
            ):
        self._product_service = product_service
        self._saga_service = saga_service
        self.media_service: MediaService = media_service
        
    async def _delete_entities(self, command: UpdateProductCommand) -> None:
        images_to_delete = await self._product_service.delete_existing_entities(command)

        self._saga_service.add_step(
            action=self.media_service.move_images_to_trash,
            action_kwargs={
                "images_public_id": images_to_delete
            },
            action_name="move_images_to_trash",
            compensation=self.media_service.recover_images_from_trash,
            compensation_kwargs={
                "images_public_id": images_to_delete
            },
            compensation_name="recover_images_from_trash"
        )
        await self._saga_service.execute_last()
        return None


    async def execute(
            self,
            command: UpdateProductCommand,
            product_id: int,
            new_images_file: List[BinaryIO] | None = None,
    ) -> None:
        if command.has_all_variants_deleted:
            raise ValidationError(
                "Product need at least one variant",
                {
                    "event": "update_product_case/execute",
                    "product_id": product_id
                }
            )
        self._product_service.validate_product_form(new_images_file, command)
        
        try:
            await self._delete_entities(command)

            images = None
            if new_images_file is not None and command.temp_keys is not None:
                images = await self._product_service.upload_images_by_temp_key(
                    self._saga_service,
                    new_images_file,
                    command.temp_keys,
                    self.media_service.upload_images_batch,
                    self.media_service.move_images_to_trash
                )

            await self._product_service.update_product_with_variants(
                product_id,
                command,
                images
            )
        except AppException as ae:
            await self._saga_service.compensate_all()

            ae.context["compensation_errors"] = self._saga_service.compensation_errors

            raise ae
