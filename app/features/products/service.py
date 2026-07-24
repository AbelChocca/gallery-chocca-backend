from app.infra.db.repositories.product_repository import PostgresProductRepository
from app.features.products.product_dto import PublishProductCommand
from app.shared.slug.protocol import SlugProtocol
from app.features.products.product import Product
from app.features.products.product_dto import (
    UpdateProductCommand, 
    FilterProductCommand, 
    CountProductPerCategoryDTO, 
    CatalogProductDTO,
)
from app.core.exceptions import ValidationError

class ProductService:
    def __init__(
            self,
            product_repo: PostgresProductRepository,
            slug_service: SlugProtocol,
        ):
        self._product_repo: PostgresProductRepository = product_repo
        self._slug_service: SlugProtocol = slug_service


    async def get_variant_size_by_id(
        self,
        variant_size_id: int,
    ):
        return await self._product_repo.get_variant_size_by_id(
            variant_size_id
        )
    
    async def get_product_entity_by_id(
        self,
        product_id: int,
    ) -> Product:
        return await self._product_repo.get_by_id(
            product_id
        )
    
    async def create_product(
        self,
        command: PublishProductCommand
    ) -> Product:

        product = Product(
            nombre=command.nombre,
            descripcion=command.descripcion,
            marca=command.marca,
            categoria=command.categoria,
            model_family=command.model_family,
            fit=command.fit,
            slug=self._slug_service.generate(
                command.nombre
            ),
            variants=[]
        )


        for variant in command.variants:
            product.add_variant(
                variant_command=variant
            )


        return await self._product_repo.save(
            product,
            flush=True
        )
    
    async def update_product(
        self,
        product_id: int,
        command: UpdateProductCommand
    ) -> Product:

        product = await self.get_product_entity_by_id(
            product_id
        )

        if not product.is_active:
            raise ValidationError(
                "El producto esta deshabilitado temporalmente.",
                {
                    "product_id": product_id
                }
            )


        if command.name_changed:
            product.slug = self._slug_service.generate(
                command.nombre
            )


        product.update_product(
            command.to_dict
        )


        return await self._product_repo.save(
            product
        )
    
    async def get_related_products(
        self,
        query: str,
        limit: int
    ) -> list[Product]:

        return await self._product_repo.search_related(
            query,
            0,
            limit
        )

    async def delete_product(
        self,
        product_id: int
    ) -> None:
        await self._product_repo.delete_by_id(product_id)
    
    async def _count_by_category(self) -> list[CountProductPerCategoryDTO]:
        res = await self._product_repo.get_count_by_category()

        products_per_category: list[CountProductPerCategoryDTO] = [
            CountProductPerCategoryDTO(
                total=total,
                category=category
            )
            for category, total in res
        ]

        return products_per_category
    
    async def _get_last_n(self, n: int) -> list[dict]:
        last_n_products = await self._product_repo.get_last_n_products(n)
        if not last_n_products: 
            return []

        return [
            product.to_dict
            for product in last_n_products
        ]

    async def get_products(
        self,
        command: FilterProductCommand,
        offset: int,
        limit: int,
    ) -> Product:
        
        return await self._product_repo.get_all(
            command,
            offset,
            limit,
        )

    async def count_products(
        self,
        command: FilterProductCommand | None = None,
    ) -> int:
        return await self._product_repo.count_filtered_products(command)