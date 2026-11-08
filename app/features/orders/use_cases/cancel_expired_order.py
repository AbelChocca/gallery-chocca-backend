from app.features.orders.services.order_service import (
    OrderService,
)

from app.features.inventory.services.inventory_service import (
    InventoryService,
)
from app.features.inventory.services.inventory_movement_service import (
    InventoryMovementService,
)

from app.features.inventory.types.inventory_movement import (
    InventoryMovementType
)
from app.features.inventory.types.inventory_reference import InventoryReferenceType
from app.features.inventory.dtos.inventory import InventoryReservedItem 



class CancelExpiredOrderUseCase:
    def __init__(
        self,
        *,
        order_service: OrderService,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
    ) -> None:
        self._order_service = order_service
        self._inventory_service = inventory_service
        self._inventory_movement_service = (
            inventory_movement_service
        )

    async def execute(
        self,
        *,
        order_id: int,
    ) -> None:
        order = await (
            self._order_service
            .cancel_expired_order_by_id(
                order_id=order_id,
                flush=True,
            )
        )

        reservation_movements = await (
            self._inventory_movement_service
            .get_by_reference(
                reference_type=(
                    InventoryReferenceType.ORDER
                ),
                reference_id=order.id,
                movement_type=(
                    InventoryMovementType.RESERVATION
                ),
            )
        )

        if not reservation_movements:
            return

        reserved_items = [
            InventoryReservedItem(
                owner_type=movement.owner_type,
                owner_id=movement.owner_id,
                location_id=movement.location_id,
                quantity=movement.quantity,
            )
            for movement in reservation_movements
        ]

        release_results = await (
            self._inventory_service
            .release_reserved_stock(
                items=reserved_items
            )
        )

        movements_by_key = {
            (
                movement.owner_type,
                movement.owner_id,
                movement.location_id,
            ): movement
            for movement in reservation_movements
        }

        for result in release_results:
            original = movements_by_key[
                (
                    result.owner_type,
                    result.owner_id,
                    result.location_id,
                )
            ]

            await (
                self._inventory_movement_service
                .create_movement(
                    movement_type=(
                        InventoryMovementType
                        .RESERVATION_RELEASE
                    ),
                    owner_type=result.owner_type,
                    owner_id=result.owner_id,
                    location_id=result.location_id,
                    owner_name=original.owner_name,
                    owner_code=original.owner_code,
                    quantity=result.quantity,
                    prev_stock=(
                        result.previous_stock
                    ),
                    new_stock=(
                        result.current_stock
                    ),
                    reference_type=(
                        InventoryReferenceType.ORDER
                    ),
                    reference_id=order.id,
                    reason=(
                        "Reserva liberada por "
                        "expiración del pedido."
                    ),
                )
            )