import pytest_asyncio
from app.features.inventory.resolvers.material_owner import (
    MaterialOwnerResolver
)

from sqlmodel import SQLModel
from tests.conf.db_test import engine
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.material.service import MaterialService

from app.shared.pagination.pagination_service import PaginationService
from app.infra.db.repositories.material_repository import PostgresMaterialRepository
from app.infra.db.models.model_material import MaterialTable
from app.infra.db.mappers.material_mapper import MaterialMapper

from app.infra.db.repositories.sqlalchemy_inventory_movement_repo import PostgresInventoryMovementReposity
from app.infra.db.models.model_inventory_movement import InventoryMovementTable
from app.infra.db.mappers.inventory_movement_mapper import InventoryMovementMapper
from app.features.inventory.inventory_service import InventoryService

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

@pytest_asyncio.fixture
def inventory_service(db_session):

    repository = PostgresInventoryMovementReposity(
        db_session=db_session,
        base_mapper=InventoryMovementMapper,
        base_model=InventoryMovementTable
    )

    return InventoryService(
        inventory_movement_repo=repository,
        pagination_service=PaginationService()
    )

@pytest_asyncio.fixture
def material_owner_resolver(material_service):
    return MaterialOwnerResolver(
        material_service=material_service
    )