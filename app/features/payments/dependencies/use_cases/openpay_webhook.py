from typing import Annotated

from fastapi import Depends

from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.dependencies.services import (
    get_order_service,
)

from app.features.payments.services.payment_service import (
    PaymentService,
)
from app.features.payments.services.payment_event_service import (
    PaymentEventService,
)
from app.features.payments.dependencies.services import (
    get_payment_service,
    get_payment_event_service,
)

from app.features.inventory.services.inventory_service import (
    InventoryService,
)
from app.features.inventory.dependencies.services import (
    get_inventory_service,
)

from app.features.inventory.services.inventory_movement_service import (
    InventoryMovementService,
)
from app.features.inventory.dependencies.services import (
    get_inventory_movement_service,
)

from app.features.payments.use_cases.openpay_webhook import (
    ProcessOpenpayWebhookUseCase,
)


def get_process_openpay_webhook_use_case(
    payment_service: Annotated[
        PaymentService,
        Depends(get_payment_service),
    ],
    payment_event_service: Annotated[
        PaymentEventService,
        Depends(get_payment_event_service),
    ],
    order_service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
    inventory_service: Annotated[
        InventoryService,
        Depends(get_inventory_service),
    ],
    inventory_movement_service: Annotated[
        InventoryMovementService,
        Depends(get_inventory_movement_service),
    ],
) -> ProcessOpenpayWebhookUseCase:
    return ProcessOpenpayWebhookUseCase(
        payment_service=payment_service,
        payment_event_service=payment_event_service,
        order_service=order_service,
        inventory_service=inventory_service,
        inventory_movement_service=inventory_movement_service,
    )