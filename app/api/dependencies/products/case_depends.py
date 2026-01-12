from app.application.products.cases.create_product import CreateProductUseCase
from app.application.products.cases.delete_product import DeleteProductCase
from app.application.products.cases.get_products import GetProductsCase
from app.application.products.cases.update_product import UpdateProductCase
from app.application.products.cases.get_product_by_id import GetProductByIDCase
from app.application.products.cases.search_product import SearchProductCase

from app.infra.media.cloudinary_service import CloudinaryService
from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.cache.redis_service import RedisService 
from app.core.settings.pydantic_settings import Settings
from app.core.log.protocole import LoggerProtocol
from app.shared.services.slug.protocol import SlugProtocol

from app.core.settings.pydantic_settings import get_settings
from app.api.dependencies.products.repo import get_product_repo
from app.api.dependencies.media.service import get_media_service
from app.api.dependencies.media.repo import get_image_repo
from app.api.dependencies.cache.service import get_cache_service
from app.core.log.loguru_service import get_logger_service
from app.shared.services.slug.slugify_service import get_slugify_service

from fastapi import Depends

def get_create_product_case(
    product_repo: PostgresProductRepository = Depends(get_product_repo),
    media_service: CloudinaryService = Depends(get_media_service),
    image_repo: PostgresImageRepository = Depends(get_image_repo),
    logger: LoggerProtocol = Depends(get_logger_service),
    cache_service: RedisService = Depends(get_cache_service),
    slug_service: SlugProtocol = Depends(get_slugify_service)
) -> CreateProductUseCase:
    return CreateProductUseCase(
        product_repo=product_repo,
        image_repo=image_repo,
        media_service=media_service,
        slug_service=slug_service,
        cache_service=cache_service,
        logger=logger
        )

def get_product_by_id_case(
    product_repo: PostgresProductRepository = Depends(get_product_repo),
    image_repo: PostgresImageRepository = Depends(get_image_repo),
    cache_repo: RedisService = Depends(get_cache_service),
    settings_repo: Settings = Depends(get_settings),
    logger: LoggerProtocol = Depends(get_logger_service)
) -> CreateProductUseCase:
    return GetProductByIDCase(
        product_repo=product_repo,
        image_repo=image_repo,
        cache_service=cache_repo,
        settings_repo=settings_repo,
        logger=logger
    )

def get_delete_product_case(
    product_repo: PostgresProductRepository = Depends(get_product_repo),
    image_repo: PostgresImageRepository = Depends(get_image_repo),
    media_service: CloudinaryService = Depends(get_media_service),
    cache_service: RedisService = Depends(get_cache_service),
    logger:  LoggerProtocol = Depends(get_logger_service)
) -> DeleteProductCase:
    return DeleteProductCase(
        product_repo=product_repo, 
        image_repo=image_repo,
        media_service=media_service, 
        logger=logger, 
        cache_service=cache_service
        )

def get_all_products_case(
    product_repo: PostgresProductRepository = Depends(get_product_repo),
    image_repo: PostgresImageRepository = Depends(get_image_repo),
    cache_service: RedisService = Depends(get_cache_service),
    settings: Settings = Depends(get_settings),
    logger: LoggerProtocol = Depends(get_logger_service)
) -> GetProductsCase:
    return GetProductsCase(
        product_repo=product_repo,
        image_repo=image_repo,
        cache_service=cache_service,
        settings=settings,
        logger=logger
    )

def get_update_product_case(
    product_repo: PostgresProductRepository = Depends(get_product_repo),
    image_repo: PostgresImageRepository = Depends(get_image_repo),
    logger: LoggerProtocol = Depends(get_logger_service),
    media_service: CloudinaryService = Depends(get_media_service),
    cache_service: RedisService = Depends(get_cache_service),
    slug_service: SlugProtocol = Depends(get_slugify_service)
) -> UpdateProductCase:
    return UpdateProductCase(
        product_repo=product_repo,
        image_repo=image_repo,
        logger=logger,
        media_service=media_service,
        cache_service=cache_service,
        slug_service=slug_service
        )

def get_search_products_case(
        product_repo: PostgresProductRepository = Depends(get_product_repo),
        image_repo: PostgresImageRepository = Depends(get_image_repo)
) -> SearchProductCase:
    return SearchProductCase(
        product_repo=product_repo,
        image_repo=image_repo
        )