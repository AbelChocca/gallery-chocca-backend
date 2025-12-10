from app.modules.product.domain.use_cases.create_product import CreateProductUseCase
from app.modules.product.domain.use_cases.delete_product import DeleteProductCase
from app.modules.product.domain.use_cases.get_products import GetProductsCase
from app.modules.product.domain.use_cases.update_product import UpdateProductCase
from app.modules.product.domain.use_cases.get_product_by_id import GetProductByIDCase
from app.modules.product.domain.use_cases.delete_image_product import DeleteImageProductCase
from app.modules.product.domain.use_cases.delete_variant_product import DeleteProductVariantCase
from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.core.log.repository_logger import LoggerRepository

from app.modules.product.interface.dependencies.repo import get_product_repo
from app.core.log.logger_repository_loguru import get_logger_repo

from fastapi import Depends

def get_create_product_case(
    product_repo: ProductRepository = Depends(get_product_repo),
    logger: LoggerRepository = Depends(get_logger_repo)
) -> CreateProductUseCase:
    return CreateProductUseCase(product_repo, logger)

def get_product_by_id_case(
    product_repo: ProductRepository = Depends(get_product_repo)
) -> CreateProductUseCase:
    return GetProductByIDCase(product_repo)

def get_delete_image_by_id_case(
    product_repo: ProductRepository = Depends(get_product_repo)
) -> DeleteImageProductCase:
    return DeleteImageProductCase(product_repo)

def get_delete_product_case(
    product_repo: ProductRepository = Depends(get_product_repo),
    logger:  LoggerRepository = Depends(get_logger_repo)
) -> DeleteProductCase:
    return DeleteProductCase(product_repo, logger)

def get_all_products_case(
    product_repo: ProductRepository = Depends(get_product_repo)
) -> GetProductsCase:
    return GetProductsCase(product_repo)

def get_update_product_case(
    product_repo: ProductRepository = Depends(get_product_repo),
    logger: LoggerRepository = Depends(get_logger_repo)
) -> UpdateProductCase:
    return UpdateProductCase(product_repo, logger)

def get_delete_variant_by_id(
    product_repo: ProductRepository = Depends(get_product_repo)
) -> DeleteProductVariantCase:
    return DeleteProductVariantCase(product_repo)