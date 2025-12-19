from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.entities.product_variant import ProductVariant
from app.modules.product.domain.entities.variant_image import VariantImage
from app.modules.product.domain.dto.product_dto import ReadProductDTO, FilterSchemaDTO, UpdateProductDTO
from app.modules.product.domain.dto.variant_dto import ReadProductVariantDTO, UpdateProductVariantDTO
from app.modules.product.domain.dto.variant_image_dto import UpdateVariantImageDTO
from app.modules.product.domain.dto.variant_image_dto import ReadVariantImageDTO
from app.application.products.commands import FilterProductCommand, UpdateProductCommand

from typing import Dict, Any

class ProductCommandToDTOMapper:
    @staticmethod
    def to_filter_dto(command: FilterProductCommand)-> FilterSchemaDTO:
        return FilterSchemaDTO(
            name=command.name,
            marca=command.marca,
            categoria=command.categoria,
            modelo=command.modelo,
            minPrice=command.minPrice,
            maxPrice=command.maxPrice,
            color=command.color,
            promocion=command.promocion
        )
    @staticmethod
    def to_update_dto(command: UpdateProductCommand) -> UpdateProductDTO:
        return UpdateProductDTO(
            nombre=command.nombre,
            descripcion=command.descripcion,
            marca=command.marca,
            categoria=command.categoria,
            modelo=command.modelo,
            precio=command.precio,
            descuento=command.descuento,
            promocion=command.promocion,
            variants=[
                UpdateProductVariantDTO(
                    id=variant.id,
                    color=variant.color,
                    tallas=variant.tallas,
                    to_delete=variant.to_delete,
                    imagenes=[
                        UpdateVariantImageDTO(
                            to_delete=image.to_delete,
                            cloudinary_id=image.cloudinary_id
                        )
                        for image in variant.imagenes
                    ]
                )
                for variant in command.variants
            ]
        )

class ProductEntityToDTOMapper:
    @staticmethod
    def to_read_dto(entity: Product) -> ReadProductDTO:
        return ReadProductDTO(
            id=entity.id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            categoria=entity.categoria,
            marca=entity.marca,
            modelo=entity.modelo,
            precio=entity.precio,
            descuento=entity.descuento,
            slug=entity.slug,
            promocion=entity.promocion,
            variants=[
                ReadProductVariantDTO(
                    id=variant.id,
                    product_id=variant.product_id,
                    color=variant.color,
                    tallas=variant.tallas,
                    imagenes=[
                        ReadVariantImageDTO(
                            id=image.id,
                            variant_id=image.variant_id,
                            url=image.url,
                            cloudinary_id=image.cloudinary_id
                        )
                        for image in variant.imagenes
                    ]
                )
                for variant in entity.variants
            ]
        )
    
class ProductEntityToDictMapper:
    @staticmethod
    def dict_to_product(d: dict) -> Product:
        variants = [
            ProductVariant(
                color=v["color"],
                tallas=v["tallas"],
                imagenes=[
                    VariantImage(url=i["url"], cloudinary_id=i["cloudinary_id"], id=i.get("id"), variant_id=i.get("variant_id"))
                    for i in v.get("imagenes", [])
                ],
                id=v.get("id"),
                product_id=v.get("product_id")
            )
            for v in d.get("variants", [])
        ]
        return Product(
            nombre=d["nombre"],
            descripcion=d["descripcion"],
            precio=d["precio"],
            categoria=d["categoria"],
            slug=d["slug"],
            variants=variants,
            modelo=d.get("modelo"),
            id=d.get("id"),
            descuento=d.get("descuento", 0.0),
            marca=d.get("marca"),
            promocion=d.get("promocion", False)
        )

    @staticmethod
    def to_read_dict(entity: Product) -> Dict[str, Any]:
        return {
            "id": entity.id,
            "nombre": entity.nombre,
            "descripcion": entity.descripcion,
            "precio": entity.precio,
            "descuento": entity.descuento,
            "marca": entity.marca,
            "categoria": entity.categoria,
            "modelo": entity.modelo,
            "promocion": entity.promocion,
            "slug": entity.slug,
            "variants": [
                {
                    "id": variant.id,
                    "color": variant.color,
                    "tallas": variant.tallas,
                    "product_id": variant.product_id,
                    "imagenes": [
                        {
                            "id": img.id,
                            "url": img.url,
                            "cloudinary_id": img.cloudinary_id,
                            "variant_id": img.variant_id
                        } for img in variant.imagenes
                    ]
                } for variant in entity.variants
            ]
        }