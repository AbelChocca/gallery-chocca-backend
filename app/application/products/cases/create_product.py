from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.domain.media.protocol import MediaProtocol
from app.domain.cache.protocole import CacheProtocol
from app.core.log.protocole import LoggerProtocol
from app.shared.services.slug.protocol import SlugProtocol

from app.domain.product.entities.product import Product
from app.domain.product.entities.product_variant import ProductVariant
from app.domain.product.dto.product_dto import ReadProductDTO
from app.application.products.commands import PublishProductCommand
from app.application.products.exceptions import MissMatchLength
from app.application.products.helper_mapper import ProductEntityToDTOMapper

from typing import List, BinaryIO


class CreateProductUseCase:
    def __init__(
            self, 
            product_repo: PostgresProductRepository,
            image_repo: PostgresImageRepository,
            media_service: MediaProtocol,
            slug_service: SlugProtocol,
            cache_service: CacheProtocol,
            logger: LoggerProtocol
            ):
        self.product_repo = product_repo
        self.image_repo = image_repo
        self.logger = logger
        self.media_service = media_service
        self.cache_service = cache_service
        self.slug_service = slug_service

    async def execute(
            self, 
            images_file: List[BinaryIO],
            command: PublishProductCommand
            ) -> ReadProductDTO:
        self.logger.info(f"Start publishing the product: {command.nombre}")
        if len(images_file) != len(command.temp_variants_id):
            raise MissMatchLength("Length of image list and his temp's id aren't match")
        
        product_variants = [
            ProductVariant(
                color=variant.color,
                tallas=variant.tallas
            )
            for variant in (command.variants or [])
        ]
        new_product = Product(
            nombre=command.nombre,
            descripcion=command.descripcion,
            precio=command.precio,
            marca=command.marca,
            categoria=command.categoria,
            modelo=command.modelo,
            descuento=command.descuento,
            variants=product_variants,
            slug=self.slug_service.generate(command.nombre),
            promocion=command.promocion
        )
        new_product.raise_invalid_variants_index(command.temp_variants_id)

        new_product = await self.product_repo.save(new_product)
        
        for file, variant_index in zip(images_file, command.temp_variants_id):
            cloud_image = self.media_service.upload_image(
                file=file,
                folder="products"
            )

            new_product.add_image_on_specify_variant(
                variant_index=variant_index,
                image_url=cloud_image.url,
                service_id=cloud_image.public_id
                )
            
        new_images = await self.image_repo.save_many(
            entities=new_product.get_all_images_from_variants()
        )
        new_product.sync_images_id(new_images)
        # Invalidating cache
        await self.cache_service.cache_delete(Product.get_filter_key(category=new_product.categoria))

        self.logger.info(f"Product {new_product.nombre} with id: {new_product.id} was successfully saved.")

        return ProductEntityToDTOMapper.to_read_dto(new_product)