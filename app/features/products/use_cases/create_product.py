from app.infra.saga.saga_use_case import UseCaseSaga
from app.infra.saga.saga_service import SagaService
from app.features.products.service import ProductService
from app.infra.cache.redis_service import RedisService
from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.services.inventory_movement_service import InventoryMovementService
from app.features.media.service import MediaService
from app.features.products.product import Product
from app.features.products.constants import PRODUCT_CACHE_KEY_TAG
from app.core.exceptions import ValidationError
from app.features.products.product_dto import CreateProductResponseDTO
from app.features.media.types import StorageFolder, ImageType
from app.features.inventory.types.inventory_movement import InventoryOwnerType, InventoryMovementType
from app.features.products.product_dto import PublishProductCommand
from app.features.inventory.dtos.inventory import CreateInventoryCommand
from app.features.products.variant_size.variant_size import VariantSize

from typing import BinaryIO
from decimal import Decimal

class CreateProductUseCase(UseCaseSaga):

    def __init__(
        self,
        saga_service: SagaService,
        product_service: ProductService,
        media_service: MediaService,
        cache_service: RedisService,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService
    ):
        super().__init__(saga_service)

        self._product_service = product_service
        self._media_service = media_service
        self._cache_service = cache_service
        self._inventory_service = inventory_service
        self._inventory_movement_service = inventory_movement_service


    async def execute(
        self,
        images_file: list[BinaryIO],
        command: PublishProductCommand,
        user_id: int,
    ) -> CreateProductResponseDTO:

        async def operation():

            self._validate_images(
                images_file,
                command,
            )

            product = await self._product_service.create_product(
                command
            )

            await self._create_initial_inventory(
                product=product,
                command=command,
                user_id=user_id,
            )

            await self._upload_variant_images(
                product=product,
                command=command,
                images_file=images_file,
            )

            await self._cache_service.invalidate_entities(
                PRODUCT_CACHE_KEY_TAG
            )

            return CreateProductResponseDTO(
                id=product.id,
                slug=product.slug,
            )

        return await self._saga.execute_safely(operation)
    
    def _map_variant_images(
        self,
        images_file: list[BinaryIO],
        image_temp_keys: list[str],
        command: PublishProductCommand,
        product: Product,
    ) -> dict[int, list[BinaryIO]]:

        if not images_file or not image_temp_keys:
            return {}

        variant_color_mapping = {
            variant.color: variant.id
            for variant in product.variants
        }

        # temp_key -> variant_id
        variant_mapping = {}

        for variant_command in command.variants:

            variant_id = variant_color_mapping.get(
                variant_command.color
            )

            if variant_id is None:
                raise ValidationError(
                    "Variant color was not found after product creation",
                    {
                        "event": "create_product_use_case/image_mapping",
                        "color": variant_command.color
                    }
                )

            variant_mapping[
                variant_command.temp_key
            ] = variant_id

        # variant_id -> images
        images_by_variant: dict[int, list[BinaryIO]] = {}


        for image, temp_key in zip(
            images_file,
            image_temp_keys
        ):

            variant_id = variant_mapping.get(
                temp_key
            )

            if variant_id is None:
                raise ValidationError(
                    "Image temp key doesn't match any product variant",
                    {
                        "event": "create_product_use_case/image_mapping",
                        "temp_key": temp_key
                    }
                )


            images_by_variant.setdefault(
                variant_id,
                []
            ).append(
                image
            )


        return images_by_variant
    
    async def _create_initial_inventory(
        self,
        *,
        product: Product,
        command: PublishProductCommand,
        user_id: int,
    ) -> None:

        inventory_mapping = {
            (
                variant.temp_key,
                size.size,
            ): size.inventories
            for variant in command.variants
            for size in variant.sizes
        }

        variant_command_by_temp = {
            variant.temp_key: variant
            for variant in command.variants
        }

        for variant in product.variants:

            variant_command = variant_command_by_temp[
                variant.temp_key
            ]

            for size in variant.sizes:

                inventories = inventory_mapping[
                    (
                        variant_command.temp_key,
                        size.size,
                    )
                ]

                await self._create_inventory_for_size(
                    product=product,
                    variant_size=size,
                    inventories=inventories,
                    user_id=user_id,
                )

    async def _create_inventory_for_size(
        self,
        *,
        product: Product,
        variant_size: VariantSize,
        inventories: list[CreateInventoryCommand],
        user_id: int,
    ) -> None:

        for inv in inventories:

            await self._inventory_service.create_inventory(
                owner_type=InventoryOwnerType.PRODUCT,
                owner_id=variant_size.id,
                location_id=inv.location_id,
                minimum_stock=inv.minimum_stock,
            )

            if inv.initial_stock is None:
                continue

            await self._inventory_movement_service.create_movement(
                movement_type=InventoryMovementType.ENTRY,
                owner_type=InventoryOwnerType.PRODUCT,
                owner_id=variant_size.id,
                location_id=inv.location_id,
                owner_name=product.nombre,
                owner_code=variant_size.sku,
                quantity=inv.initial_stock,
                prev_stock=Decimal("0"),
                new_stock=inv.initial_stock,
                performed_by=user_id,
                reason="Entrada de stock de prenda.",
            )

    async def _upload_variant_images(
        self,
        *,
        product: Product,
        command: PublishProductCommand,
        images_file: list[BinaryIO],
    ) -> None:

        images_by_variant = self._map_variant_images(
            images_file,
            command.temp_keys,
            command,
            product,
        )

        for variant in product.variants:

            images = images_by_variant.get(
                variant.id,
                [],
            )

            if not images:
                continue

            uploads = await self._upload_images(
                images
            )

            await self._media_service.create_image_batch(
                uploads=uploads,
                owner_id=variant.id,
                owner_type=ImageType.variant,
            )

    async def _upload_images(
        self,
        images: list[BinaryIO],
    ):

        return await self._saga.execute_step(
            action=self._media_service.upload_images_batch,
            action_kwargs={
                "images_resource": images,
                "folder": StorageFolder.PRODUCTS,
            },
            compensation_factory=lambda uploaded: (
                self._media_service.move_images_to_trash,
                self._media_service.move_images_to_trash.__name__,
                {
                    "images_public_id": [
                        image.public_id
                        for image in uploaded
                    ]
                },
            ),
        )
    
    def _validate_images(
        self,
        images_file: list[BinaryIO] | None,
        command: PublishProductCommand,
    ) -> None:

        if (
            images_file is not None
            and command.temp_keys is not None
            and len(images_file) != len(command.temp_keys)
        ):
            raise ValidationError(
                "Length of image list and temp keys don't match",
                {
                    "event": "create_product_use_case/image_validation",
                    "image_count": len(images_file),
                    "temp_keys_count": len(command.temp_keys),
                },
            )