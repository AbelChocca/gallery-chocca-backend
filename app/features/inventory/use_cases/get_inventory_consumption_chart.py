from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from app.core.exceptions import ValueNotFound
from app.features.inventory.dtos.inventory import (
    InventoryConsumptionChartDTO,
    InventoryConsumptionPointDTO,
)
from app.features.inventory.dtos.inventory_movements import (
    InventoryMovementFilters,
)
from app.features.inventory.services.inventory_movement_service import (
    InventoryMovementService,
)
from app.features.inventory.types.inventory_movement import (
    InventoryMovementType,
    InventoryOwnerType,
)
from app.features.inventory.resolvers.inventory_owner_resolver import InventoryOwnerResolverService


class GetInventoryConsumptionChartUseCase:

    def __init__(
        self,
        inventory_movement_service: InventoryMovementService,
        inventory_owner_resolver: InventoryOwnerResolverService,
    ) -> None:
        self._inventory_movement_service = (
            inventory_movement_service
        )
        self._inventory_owner_resolver = (
            inventory_owner_resolver
        )

    async def execute(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
        current_location_id: int,
        days: int = 30,
    ) -> InventoryConsumptionChartDTO:

        owner = await self._inventory_owner_resolver.resolve(
            owner_type=owner_type,
            owner_id=owner_id,
        )

        if owner is None:
            raise ValueNotFound(
                "La entidad propietaria del inventario no se pudo encontrar.",
                {
                    "owner_type": owner_type.value,
                    "owner_id": owner_id,
                },
            )

        now = datetime.now(timezone.utc)

        start_date = (
            now - timedelta(days=days - 1)
        ).date()

        movements = await (
            self._inventory_movement_service
            .get_inventory_movements(
                filter_command=InventoryMovementFilters(
                    owner_type=owner_type,
                    owner_id=owner_id,
                    type=InventoryMovementType.USAGE,
                    from_date=datetime.combine(
                        start_date,
                        datetime.min.time(),
                        tzinfo=timezone.utc,
                    ),
                    to_date=now,
                )
            )
        )

        consumption_by_date: dict[date, Decimal] = {}

        for movement in movements:
            movement_date = movement.created_at.date()

            consumption_by_date[movement_date] = (
                consumption_by_date.get(
                    movement_date,
                    Decimal("0"),
                )
                + abs(movement.quantity)
            )

        points = [
            InventoryConsumptionPointDTO(
                date=current_date,
                quantity=consumption_by_date.get(
                    current_date,
                    Decimal("0"),
                ),
            )
            for i in range(days)
            for current_date in [
                start_date + timedelta(days=i)
            ]
        ]

        return InventoryConsumptionChartDTO(
            unit_type=owner.unit_type,
            points=points,
        )