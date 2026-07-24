import pytest_asyncio

from sqlmodel import SQLModel
from tests.config.db_test import engine
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.material.service import MaterialService

from app.shared.pagination.pagination_service import PaginationService
from app.features.material.material_repository import PostgresMaterialRepository
from app.features.material.models.model_material import MaterialTable
from app.infra.db.mappers.material_mapper import MaterialMapper

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        session = AsyncSession(
            bind=conn,
            expire_on_commit=False
        )

        try:
            yield session
        finally:
            await session.close()

@pytest_asyncio.fixture
def uow_factory(db_session):
    def create_uow():
        return UnitOfWork(lambda: db_session)

    return create_uow

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