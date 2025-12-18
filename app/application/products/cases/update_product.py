from app.modules.product.domain.dto.product_dto import ReadProductDTO
from app.modules.product.domain.exceptions.variant_exception import InvalidImageVariantMapping
from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.core.log.logger_repository import LoggerRepository
from app.shared.services.slug.domain.slug_repository import SlugRepository
from app.application.products.commands import UpdateProductCommand
from app.application.products.helper_mapper import ProductCommandToDTOMapper, ProductEntityToDTOMapper

from typing import BinaryIO, List, Optional

class UpdateProductCase:
    def __init__(
            self,
            repo: ProductRepository,
            logger: LoggerRepository,
            image_repo: CloudinaryRepository,
            slug_repo: SlugRepository
            ):
        self.repo: ProductRepository = repo
        self.logger: LoggerRepository = logger
        self.image_repo: CloudinaryRepository = image_repo
        self.slug_repo: SlugRepository = slug_repo

    async def execute(
            self,
            command: UpdateProductCommand,
            product_id: int,
            new_images_file: Optional[List[BinaryIO]] = None,
    ) -> ReadProductDTO:
        if len(new_images_file) != len(command.temp_variants_id):
            raise InvalidImageVariantMapping("Missing match length of the new_images_file and temp_variants_id")
        
        existing_product = await self.repo.get_by_id(product_id)
        self.logger.info(f"Start updating the product {existing_product.nombre} with id: {product_id}")

        update_variants_dto = ProductCommandToDTOMapper.to_update_dto(command).variants

        existing_product.sync_variants(update_variants_dto)
        existing_product.raise_invalid_variants_index(command.temp_variants_id)

        if new_images_file is not None and command.temp_variants_id is not None:
            for image, temp_id in zip(new_images_file, command.temp_variants_id):
                new_image = self.image_repo.upload_image(
                    file=image,
                    folder="products"
                )
                existing_product.add_image_on_specify_variant(
                    variant_index=temp_id,
                    url=new_image.url,
                    public_id=new_image.public_id
                )

        images_to_delete, variants_to_delete = (
            existing_product.plan_images_and_variants_deletions(update_variants_dto)
        )

        for image_id in images_to_delete:
            if image_id is not None:
                await self.repo.delete_image_by_id(image_id)
                self.image_repo.delete_image(image_id)

        for variant_id in variants_to_delete:
            if variant_id:
                await self.repo.delete_variant_by_id(variant_id)

        # Generate slug if name was update
        if command.name_changed:
            new_slug = self.slug_repo.generate(command.nombre)
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

        new_product = await self.repo.save(existing_product)

        self.logger.info(f"Product {new_product.nombre} was saved and updated successfully!")
        return ProductEntityToDTOMapper.to_read_dto(new_product)