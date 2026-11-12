# scripts/backfill_inventory_locations.py

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.config import async_session_factory

from app.features.inventory.models.inventory_location import (
    InventoryLocationTable,
)

from app.features.locations.models.locations import (
    LocationTable,
)

from app.features.locations.types import (
    LocationType,
)


def map_location_type(
    inventory_type,
) -> LocationType:

    value = (
        inventory_type.value
        if hasattr(
            inventory_type,
            "value",
        )
        else str(inventory_type)
    )

    mapping = {
        "STORE": LocationType.STORE,
        "SHOP": LocationType.STORE,

        "WORKSHOP": LocationType.WORKSHOP,
        "FACTORY": LocationType.WORKSHOP,

        "WAREHOUSE": LocationType.WAREHOUSE,
    }

    return mapping.get(
        value,
        LocationType.OTHER,
    )


async def backfill(
    session: AsyncSession,
) -> None:

    result = await session.execute(
        select(
            InventoryLocationTable
        ).order_by(
            InventoryLocationTable.id
        )
    )

    inventory_locations = (
        result.scalars().all()
    )

    created = 0
    skipped = 0

    for inventory_location in (
        inventory_locations
    ):

        # Ya migrado.
        if (
            inventory_location.location_id
            is not None
        ):
            skipped += 1
            continue

        location = LocationTable(
            name=(
                inventory_location.name
            ),

            type=map_location_type(
                inventory_location.type
            ),

            address=(
                inventory_location.address
            ),

            is_active=(
                inventory_location.is_active
            ),
        )

        session.add(
            location
        )

        # Necesitamos el ID generado,
        # pero todavía no commit.
        await session.flush()

        inventory_location.location_id = (
            location.id
        )

        created += 1

    await session.commit()

    print(
        f"Backfill terminado. "
        f"Created: {created}, "
        f"Skipped: {skipped}"
    )


async def main() -> None:

    async with (
        async_session_factory()
        as session
    ):
        try:
            await backfill(
                session
            )

        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(
        main()
    )