from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.modules.cache.cache_repository import CacheRepository
from app.core.log.logger_repository import LoggerRepository
from app.shared.services.slug.domain.slug_repository import SlugRepository

from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.entities.product_variant import ProductVariant
from app.modules.product.domain.entities.variant_image import VariantImage
from app.modules.product.domain.dto.product_dto import ReadProductDTO
from app.application.products.commands import PublishProductCommand
from app.application.products.exceptions import MissMatchLength
from app.application.products.helper_mapper import ProductEntityToDTOMapper

from typing import List, BinaryIO


class CreateProductUseCase:
    def __init__(
            self, 
            repo: ProductRepository,
            image_repo: CloudinaryRepository,
            slug_repo: SlugRepository,
            cache_repo: CacheRepository,
            logger: LoggerRepository
            ):
        self.repo = repo
        self.logger = logger
        self.image_repo = image_repo
        self.cache_repo = cache_repo
        self.slug_repo = slug_repo

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
            slug=self.slug_repo.generate(command.nombre),
            promocion=command.promocion
        )
        new_product.raise_invalid_variants_index(command.temp_variants_id)
        
        for file, variant_id in zip(images_file, command.temp_variants_id):
            cloud_image = self.image_repo.upload_image(
                file=file,
                folder="products"
            )
            new_image = VariantImage(
                url=cloud_image.url,
                cloudinary_id=cloud_image.public_id
            )
            new_product.variants[variant_id].agregar_image(
                image_url=new_image.url,
                public_id=new_image.cloudinary_id
            )

        new_product = await self.repo.save(new_product)

        # Invalidating cache
        await self.cache_repo.cache_delete(new_product.get_filter_key(slug=new_product.slug))
        await self.cache_repo.cache_delete(new_product.get_filter_key(category=new_product.categoria))

        self.logger.info(f"Product {new_product.nombre} with id: {new_product.id} was successfully saved.")

        return ProductEntityToDTOMapper.to_read_dto(new_product)