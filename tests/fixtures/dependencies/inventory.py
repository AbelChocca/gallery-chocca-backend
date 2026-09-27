import pytest_asyncio
from decimal import Decimal


from app.features.inventory.models.inventory import InventoryTable
from app.features.inventory.types.inventory_movement import InventoryOwnerType


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def variant_size_inventory(
    db_session,
    variant_size,
    location,
):
    inventory = InventoryTable(
        owner_type=InventoryOwnerType.PRODUCT,
        owner_id=variant_size.id,
        location_id=location.id,
        quantity=Decimal("20.00"),
        reserved_quantity=Decimal("0.00"),
        minimum_stock=Decimal("2.00"),
        unit_price=Decimal("100.00"),
    )

    db_session.add(inventory)

    await db_session.commit()
    await db_session.refresh(inventory)

    return inventory