# app/features/orders/dependencies/services.py

from fastapi import Depends

from app.infra.db.uow.dependency import (
    get_uow,
)
from app.infra.db.uow.unit_of_work import (
    UnitOfWork,
)

from app.features.orders.services.order_service import (
    OrderService,
)
from app.features.orders.services.order_item_service import (
    OrderItemService,
)
from app.features.orders.services.order_promotion_service import (
    OrderPromotionService,
)
from app.features.orders.services.order_address_service import (
    OrderAddressService,
)
from app.features.orders.services.order_billing_service import (
    OrderBillingService,
)
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service
from app.features.orders.services.order_receipt import (
    OrderReceiptService,
)

from app.features.orders.services.order_pickup_service import (
    OrderPickupService,
)


def get_order_service(
    uow: UnitOfWork = Depends(get_uow),
    pagination_service: PaginationService =Depends(get_pagination_service),
) -> OrderService:
    return OrderService(
        repository=uow.orders,
        pagination_service=pagination_service,
    )


def get_order_item_service(
    uow: UnitOfWork = Depends(get_uow),
) -> OrderItemService:
    return OrderItemService(
        repository=uow.order_items,
    )


def get_order_promotion_service(
    uow: UnitOfWork = Depends(get_uow),
) -> OrderPromotionService:
    return OrderPromotionService(
        repository=uow.order_promotions,
    )


def get_order_address_service(
    uow: UnitOfWork = Depends(get_uow),
) -> OrderAddressService:
    return OrderAddressService(
        repository=uow.order_addresses,
    )


def get_order_billing_service(
    uow: UnitOfWork = Depends(get_uow),
) -> OrderBillingService:
    return OrderBillingService(
        repository=uow.order_billings,
    )

def get_order_receipt_service(
    uow: UnitOfWork = Depends(get_uow),
) -> OrderReceiptService:
    return OrderReceiptService(
        repository=uow.order_receipts,
    )



def get_order_pickup_service(
    uow: UnitOfWork = Depends(get_uow),
) -> OrderPickupService:
    return OrderPickupService(
        repository=uow.order_pickups,
    )
