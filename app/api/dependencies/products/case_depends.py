from app.application.products.cases.create_product import CreateProductUseCase
from app.application.products.cases.delete_product import DeleteProductCase
from app.application.products.cases.get_products import GetProductsCase
from app.application.products.cases.update_product import UpdateProductCase
from app.application.products.cases.get_product_by_id import GetProductByIDCase
from app.application.products.cases.delete_image_product import DeleteImageProductCase
from app.application.products.cases.delete_variant_product import DeleteProductVariantCase
from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.core.log.logger_repository import LoggerRepository
from app.shared.services.slug.domain.slug_repository import SlugRepository

from app.api.dependencies.products.repo import get_product_repo
from app.api.dependencies.cloudinary.repo import get_cloudinary_repo
from app.core.log.loguru_logger_repository import get_logger_repo
from app.shared.services.slug.infraestructure.slugify_repository import get_slugify_repository

from fastapi import Depends

def get_create_product_case(
    product_repo: ProductRepository = Depends(get_product_repo),
    image_repo: CloudinaryRepository = Depends(get_cloudinary_repo),
    logger: LoggerRepository = Depends(get_logger_repo),
    slug_repo: SlugRepository = Depends(get_slugify_repository)
) -> CreateProductUseCase:
    return CreateProductUseCase(
        repo=product_repo,
        image_repo=image_repo,
        slug_repo=slug_repo,
        logger=logger
        )

def get_product_by_id_case(
    product_repo: ProductRepository = Depends(get_product_repo),
    logger: LoggerRepository = Depends(get_logger_repo)
) -> CreateProductUseCase:
    return GetProductByIDCase(product_repo, logger)

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
    product_repo: ProductRepository = Depends(get_product_repo),
    logger: LoggerRepository = Depends(get_logger_repo)
) -> GetProductsCase:
    return GetProductsCase(product_repo, logger)

def get_update_product_case(
    product_repo: ProductRepository = Depends(get_product_repo),
    logger: LoggerRepository = Depends(get_logger_repo),
    image_repo: CloudinaryRepository = Depends(get_cloudinary_repo),
    slug_repo: SlugRepository = Depends(get_slugify_repository)
) -> UpdateProductCase:
    return UpdateProductCase(
        repo=product_repo,
        logger=logger,
        image_repo=image_repo,
        slug_repo=slug_repo
        )

def get_delete_variant_by_id(
    product_repo: ProductRepository = Depends(get_product_repo)
) -> DeleteProductVariantCase:
    return DeleteProductVariantCase(product_repo)