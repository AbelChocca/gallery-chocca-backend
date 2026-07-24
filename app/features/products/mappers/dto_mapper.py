from app.features.products.product import Product
from app.features.products.variant_size.variant_size import VariantSize
from app.features.products.product_dto import GridProductDTO, ProductDetailDTO
from app.features.products.variant.variant_dto import GridProductVariantDTO, ProductVariantDTO
from app.features.products.variant_size.variant_size_dto import VariantSizeDTO
from app.features.media.dto import ReadMediaImageDTO
from app.features.products.variant.product_variant import ProductVariant
from app.features.media.entities.image import ImageEntity

class ProductMapper:

    @staticmethod
    def to_product_detail_dto(
        product: Product,
    ) -> ProductDetailDTO:

        return ProductDetailDTO(
            id=product.id,
            nombre=product.nombre,
            descripcion=product.descripcion,
            brand=product.brand,
            category=product.category,
            fit=product.fit,
            slug=product.slug,
            variants=[
                ProductMapper.to_product_variant_dto(variant)
                for variant in product.variants
            ],
        )
    
    @staticmethod
    def to_product_variant_dto(
        variant: ProductVariant,
    ) -> ProductVariantDTO:

        return ProductVariantDTO(
            id=variant.id,
            product_id=variant.product_id,
            color=variant.color,
            sizes=[
                ProductMapper.to_variant_size_dto(size)
                for size in variant.sizes
            ],
            imagenes=[
                ProductMapper.to_image_dto(image)
                for image in variant.imagenes
            ],
        )
    
    @staticmethod
    def to_variant_size_dto(
        size: VariantSize,
    ) -> VariantSizeDTO:

        return VariantSizeDTO(
            id=size.id,
            variant_id=size.variant_id,
            size=size.size,
            barcode=size.barcode,
            sku=size.sku,
        )

    @staticmethod
    def to_grid_products(
        products: list[Product],
    ) -> list[GridProductDTO]:

        return [
            ProductMapper.to_grid_product_dto(product)
            for product in products
        ]

    @staticmethod
    def to_grid_product_dto(product: Product) -> GridProductDTO:
        return GridProductDTO(
            id=product.id,
            nombre=product.nombre,
            category=product.category,
            brand=product.brand,
            fit=product.fit,
            slug=product.slug,
            variants=[
                ProductMapper.to_grid_variant_dto(v)
                for v in product.variants
            ]
        )
    
    @staticmethod
    def to_grid_variant_dto(
        variant: ProductVariant,
    ) -> GridProductVariantDTO:

        return GridProductVariantDTO(
            id=variant.id,
            imagenes=[
                ProductMapper.to_image_dto(image)
                for image in variant.imagenes
            ]
        )
    
    @staticmethod
    def to_image_dto(
        image: ImageEntity,
    ) -> ReadMediaImageDTO:

        return ReadMediaImageDTO(
            id=image.id,
            image_url=image.image_url,
            public_id=image.public_id,
            owner_id=image.owner_id,
            alt_text=image.alt_text,
            owner_type=image.owner_type
        )