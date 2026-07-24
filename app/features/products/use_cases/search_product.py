from app.features.products.service import ProductService
from app.shared.enrichers.product_enricher import ProductEnricher
from app.features.products.mappers.dto_mapper import ProductMapper
from app.features.products.product_dto import GridProductDTO


class GetRelatedProductsUseCase:

    def __init__(
        self,
        product_service: ProductService,
        product_enricher: ProductEnricher,
    ):
        self._product_service = product_service
        self._product_enricher = product_enricher


    async def execute(
        self,
        query: str,
        limit: int,
    ) -> list[GridProductDTO]:

        products = await self._product_service.get_related_products(
            query,
            limit
        )

        await self._product_enricher.attach_variant_images(
            products
        )

        return [
            ProductMapper.to_grid_products(products)
        ]