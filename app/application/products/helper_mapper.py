from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.dto.product_dto import ReadProductDTO, FilterSchemaDTO, UpdateProductDTO
from app.modules.product.domain.dto.variant_dto import ReadProductVariantDTO, UpdateProductVariantDTO
from app.modules.product.domain.dto.variant_image_dto import UpdateVariantImageDTO
from app.modules.product.domain.dto.variant_image_dto import ReadVariantImageDTO
from app.application.products.commands import FilterProductCommand, UpdateProductCommand

from typing import Dict, Any, List

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
    
    @staticmethod
    def products_to_response_dict(total_count: int, products: List[Product]) -> Dict[str, Any]:
        return {
            "total": total_count,
            "products": [
                ProductEntityToDictMapper.to_read_dict(
                    entity=product
                )
                for product in products
            ]
        }

class ProductDictToReadDTOMapper:
    @staticmethod
    def to_read_dto(d: Dict[str, Any]) -> ReadProductDTO:
        return ReadProductDTO(
            id=d["id"],
            nombre=d["nombre"],
            descripcion=d["descripcion"],
            categoria=d["categoria"],
            marca=d.get("marca"),
            modelo=d.get("modelo"),
            precio=d["precio"],
            descuento=d.get("descuento", 0.0),
            slug=d["slug"],
            promocion=d.get("promocion", False),
            variants=[
                ProductDictToReadDTOMapper._variant_to_dto(v)
                for v in d.get("variants", [])
            ],
        )

    @staticmethod
    def _variant_to_dto(v: Dict[str, Any]) -> ReadProductVariantDTO:
        return ReadProductVariantDTO(
            id=v["id"],
            product_id=v["product_id"],
            color=v["color"],
            tallas=v["tallas"],
            imagenes=[
                ProductDictToReadDTOMapper._image_to_dto(i)
                for i in v.get("imagenes", [])
            ],
        )

    @staticmethod
    def _image_to_dto(i: Dict[str, Any]) -> ReadVariantImageDTO:
        return ReadVariantImageDTO(
            id=i["id"],
            variant_id=i["variant_id"],
            url=i["url"],
            cloudinary_id=i["cloudinary_id"],
        )