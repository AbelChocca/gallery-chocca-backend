from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.types.order import (
    OrderStatus,
)

from app.features.payments.services.payment_event_service import (
    PaymentEventService,
)
from app.features.payments.services.payment_service import (
    PaymentService,
)
from app.features.payments.types.payment import (
    PaymentProvider,
)

from app.features.payments.schemas.openpay_schema import (
    OpenpayWebhookSchema,
)
from app.features.inventory.dtos.inventory import InventoryReservedItem
from app.features.inventory.types.inventory_movement import InventoryMovementType
from app.features.inventory.types.inventory_reference import InventoryReferenceType
from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.services.inventory_movement_service import InventoryMovementService

class ProcessOpenpayWebhookUseCase:

    def __init__(
        self,
        *,
        payment_service: PaymentService,
        payment_event_service: PaymentEventService,
        order_service: OrderService,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
    ) -> None:
        self._payment_service = payment_service
        self._payment_event_service = (
            payment_event_service
        )
        self._order_service = order_service

        self._inventory_service = (
            inventory_service
        )

        self._inventory_movement_service = (
            inventory_movement_service
        )

    async def execute(
        self,
        payload: OpenpayWebhookSchema,
    ) -> None:

        if payload.type == "verification":
            return

        transaction = payload.transaction

        if transaction is None:
            return

        if transaction.order_id is None:
            return

        provider_event_id = (
            f"{payload.type}:{transaction.id}"
        )

        existing_event = (
            await self._payment_event_service
            .get_by_provider_event_id(
                provider_event_id
            )
        )

        # IDEMPOTENCY
        if existing_event is not None:
            return

        payment = (
            await self._payment_service
            .get_by_provider_order_id(
                transaction.order_id,
                raises=False,
            )
        )

        await self._payment_event_service.add(
            payment_id=(
                payment.id
                if payment is not None
                else None
            ),
            provider=PaymentProvider.OPENPAY,
            event_type=payload.type,
            provider_event_id=provider_event_id,
            payload=payload.model_dump(
                mode="json"
            ),
            flush=True,
        )

        # Si no encontramos Payment, guardamos el evento
        # para trazabilidad y no rompemos el webhook.
        if payment is None:
            return

        if payload.type == "charge.succeeded":
            await self._payment_service.mark_succeeded(
                payment=payment,
                provider_payment_id=transaction.id,
                authorization=transaction.authorization,
            )

            reservation_movements = await (
                self._inventory_movement_service
                .get_by_reference(
                    reference_type=(
                        InventoryReferenceType.ORDER
                    ),
                    reference_id=payment.order_id,
                    movement_type=(
                        InventoryMovementType.RESERVATION
                    ),
                )
            )

            reservations = [
                InventoryReservedItem(
                    owner_type=movement.owner_type,
                    owner_id=movement.owner_id,
                    location_id=movement.location_id,
                    quantity=movement.quantity,
                )
                for movement in reservation_movements
            ]

            sale_results = (
                await self._inventory_service
                .consume_reserved_stock(
                    items=reservations
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

            for result in sale_results:
                original = movements_by_key[
                    (
                        result.owner_type,
                        result.owner_id,
                        result.location_id,
                    )
                ]
                
                await self._inventory_movement_service.create_movement(
                    movement_type=(
                        InventoryMovementType.SALE
                    ),
                    owner_type=result.owner_type,
                    owner_id=result.owner_id,
                    location_id=result.location_id,

                    owner_name=original.owner_name,
                    owner_code=original.owner_code,

                    quantity=result.quantity,

                    prev_stock=result.previous_stock,
                    new_stock=result.current_stock,

                    reference_type=(
                        InventoryReferenceType.ORDER
                    ),
                    reference_id=payment.order_id,

                    reason=(
                        "Venta confirmada por pago "
                        "exitoso del pedido."
                    ),
                )

            await self._order_service.update_status(
                order_id=payment.order_id,
                status=OrderStatus.CONFIRMED,
            )

            return

        if payload.type in {
            "charge.failed",
            "charge.cancelled",
        }:
            await self._payment_service.mark_failed(
                payment=payment,
                provider_payment_id=transaction.id,
                error_message=transaction.error_message
            )

            return