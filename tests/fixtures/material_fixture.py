import pytest_asyncio

from app.features.material.service import MaterialService

from app.shared.pagination.pagination_service import PaginationService
from app.features.material.material_repository import PostgresMaterialRepository
from app.features.material.models.model_material import MaterialTable
from app.infra.db.mappers.material_mapper import MaterialMapper

from app.infra.db import model_registry  # noqa: F401



@pytest_asyncio.fixture
def material_service(db_session):

    repository = PostgresMaterialRepository(
        db_session=db_session,
        base_mapper=MaterialMapper,
        base_model=MaterialTable
    )

    return MaterialService(
        material_repository=repository,
        pagination_service=PaginationService()
    )