from app.domain.product.dto.product_dto import ReadProductDTO
from app.domain.product.exceptions.variant_exception import InvalidImageVariantMapping
from app.domain.cache.protocole import CacheProtocol
from app.domain.media.protocol import MediaProtocol
from app.core.log.protocole import LoggerProtocol
from app.shared.services.slug.protocol import SlugProtocol
from app.application.products.commands import UpdateProductCommand
from app.application.products.helper_mapper import ProductCommandToDTOMapper, ProductEntityToDTOMapper
from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository

from typing import BinaryIO, List, Optional

class UpdateProductCase:
    def __init__(
            self,
            product_repo: PostgresProductRepository,
            image_repo: PostgresImageRepository,
            logger: LoggerProtocol,
            media_service: MediaProtocol,
            cache_service: CacheProtocol,
            slug_service: SlugProtocol
            ):
        self.product_repo: PostgresProductRepository = product_repo
        self.image_repo: PostgresImageRepository = image_repo
        self.logger: LoggerProtocol = logger
        self.media_service: MediaProtocol = media_service
        self.cache_service: CacheProtocol = cache_service
        self.slug_service: SlugProtocol = slug_service

    async def execute(
            self,
            command: UpdateProductCommand,
            product_id: int,
            new_images_file: Optional[List[BinaryIO]] = None,
    ) -> ReadProductDTO:
        if new_images_file is not None and command.temp_variants_id is not None and (len(new_images_file) != len(command.temp_variants_id)):
            raise InvalidImageVariantMapping("Missing match length of the new_images_file and temp_variants_id")
        
        existing_product = await self.product_repo.get_by_id(product_id)
        self.logger.info(f"Start updating the product {existing_product.nombre} with id: {product_id}")

        update_variants_dto = ProductCommandToDTOMapper.to_update_dto(command).variants
        images_to_delete, variants_to_delete = (
            existing_product.plan_images_and_variants_deletions(update_variants_dto)
        )

        existing_product.sync_variants(update_variants_dto)
        existing_product.raise_invalid_variants_index(command.temp_variants_id)
        existing_product.raise_cannot_delete_variants(variants_to_delete)
        existing_product.cannot_delete_image(images_to_delete)

        if new_images_file is not None and command.temp_variants_id is not None:
            for image, temp_id in zip(new_images_file, command.temp_variants_id):
                new_image = self.media_service.upload_image(
                    file=image,
                    folder="products"
                )
                existing_product.add_image_on_specify_variant(
                    variant_index=temp_id,
                    url=new_image.url,
                    public_id=new_image.public_id
                )

        for variant_id in variants_to_delete:
            variant_images: List[str] = existing_product.get_variant_images(variant_id)
            for image in variant_images:
                self.media_service.delete_image(image)
                await self.image_repo.delete_by_id(image)

            await self.product_repo.delete_variant_by_id(variant_id)

        for image_id in images_to_delete:
            if image_id:
                await self.image_repo.delete_by_id(image_id)
                self.media_service.delete_image(image_id)

        # Generate slug if name was update
        if command.name_changed:
            new_slug = self.slug_service.generate(command.nombre)
            existing_product.update_slug(new_slug)

        existing_product.update_product(
            nombre=command.nombre,
            descripcion=command.descripcion,
            precio=command.precio,
            categoria=command.categoria,
            modelo=command.modelo,
            descuento=command.descuento,
            marca=command.marca,
            promocion=command.promocion
        )

        new_product = await self.product_repo.save(existing_product)
        images = await self.image_repo.save_many(entities=new_product.get_all_images_from_variants())
        new_product.sync_images_to_variants(images)

        await self.cache_service.cache_delete(key=existing_product.get_filter_key(id=existing_product.id))
        await self.cache_service.cache_delete(key=existing_product.get_filter_key(category=new_product.categoria))
        await self.cache_service.cache_delete(key=existing_product.get_filter_key(category=new_product.categoria, brand=new_product.marca))

        self.logger.info(f"Product {new_product.nombre} was saved and updated successfully!")
        return ProductEntityToDTOMapper.to_read_dto(new_product)