from app.application.products.cases.create_product import CreateProductUseCase
from app.application.products.cases.delete_product import DeleteProductCase
from app.application.products.cases.get_products import GetProductsCase
from app.application.products.cases.update_product import UpdateProductCase
from app.application.products.cases.get_product_by_id import GetProductByIDCase
from app.application.products.cases.search_product import SearchProductCase

from app.api.dependencies.media.service import get_media_service

from app.application.media.service import MediaService

from app.api.dependencies.media.service import get_media_service
from app.infra.saga_service import SagaService, get_saga_service
from app.api.dependencies.products.service import get_product_service
from app.application.products.service import ProductService


from fastapi import Depends

def get_create_product_case(
    product_service: ProductService = Depends(get_product_service),
    media_service: MediaService = Depends(get_media_service),
    saga_service: SagaService = Depends(get_saga_service)
) -> CreateProductUseCase:
    return CreateProductUseCase(
        product_service=product_service,
        media_service=media_service,
        saga_service=saga_service
    )

def get_product_by_id_case(
    product_service: ProductService = Depends(get_product_service),
) -> CreateProductUseCase:
    return GetProductByIDCase(product_service)

def get_delete_product_case(
    product_service: ProductService = Depends(get_product_service),
    media_service: MediaService = Depends(get_media_service),
    saga_service: SagaService = Depends(get_saga_service)
) -> DeleteProductCase:
    return DeleteProductCase(
        product_service=product_service,
        media_service=media_service,
        saga_service=saga_service
        )

def get_all_products_case(
    product_service: ProductService = Depends(get_product_service)
) -> GetProductsCase:
    return GetProductsCase(
        product_service
    )

def get_update_product_case(
    product_service: ProductService = Depends(get_product_service),
    media_service: MediaService = Depends(get_media_service),
    saga_service: SagaService = Depends(get_saga_service)
) -> UpdateProductCase:
    return UpdateProductCase(
        product_service=product_service,
        media_service=media_service,
        saga_service=saga_service
        )

def get_search_products_case(
        product_service: ProductService = Depends(get_product_service)
) -> SearchProductCase:
    return SearchProductCase(
        product_service
        )