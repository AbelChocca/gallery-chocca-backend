import pytest_asyncio

from app.shared.slug.slugify_service import SlugService

from app.features.products.service import ProductService
from app.features.products.models.model_product import ProductTable
from app.infra.db.repositories.product_repository import PostgresProductRepository
from app.infra.db.mappers.product_mapper import ProductMapper

@pytest_asyncio.fixture
def product_service(db_session):

    repository = PostgresProductRepository(
        db_session=db_session,
        base_mapper=ProductMapper,
        base_model=ProductTable
    )

    slug_service = SlugService()

    return ProductService(
        product_repo=repository,
        slug_service=slug_service
    )