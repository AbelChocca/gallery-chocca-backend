
import pytest_asyncio

from app.shared.pagination.pagination_service import PaginationService

# Services
from app.features.inventory.services.inventory_service import (
    InventoryService,
)
from app.features.inventory.services.inventory_movement_service import (
    InventoryMovementService,
)
from app.features.locations.services.location_service import (
    LocationService,
)

# Repositories
from app.features.inventory.repositories.inventory_repository import (
    InventoryRepository,
)
from app.features.inventory.repositories.sqlalchemy_inventory_movement_repo import (
    PostgresInventoryMovementReposity,
)
from app.features.locations.repositories.location_repository import (
    LocationRepository,
)

# Models
from app.features.inventory.models.inventory import InventoryTable
from app.features.inventory.models.inventory_movement import (
    InventoryMovementTable,
)
from app.features.locations.models.locations import (
    LocationTable,
)

# Mappers
from app.features.inventory.mappers.inventory_mapper import (
    InventoryMapper,
)
from app.infra.db.mappers.inventory_movement_mapper import (
    InventoryMovementMapper,
)
from app.features.locations.mappers.location_mapper import (
    LocationMapper,
)

@pytest_asyncio.fixture
def inventory_service(db_session):

    repository = InventoryRepository(
        db_session=db_session,
        base_mapper=InventoryMapper,
        base_model=InventoryTable,
    )

    return InventoryService(
        inventory_repository=repository,
    )


@pytest_asyncio.fixture
def inventory_location_service(db_session):

    repository = LocationRepository(
        db_session,
        LocationMapper,
        LocationTable,
    )

    return LocationService(
        repository=repository,
    )



@pytest_asyncio.fixture
def inventory_movement_service(db_session):

    repository = PostgresInventoryMovementReposity(
        db_session=db_session,
        base_mapper=InventoryMovementMapper,
        base_model=InventoryMovementTable,
    )

    return InventoryMovementService(
        inventory_movement_repo=repository,
        pagination_service=PaginationService(),
    )