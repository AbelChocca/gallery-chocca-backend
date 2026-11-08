from fastapi import Depends

from app.features.cart.dependencies.services import (
    get_cart_service,
)
from app.features.cart.service import (
    CartService,
)

from app.features.customer.customer_service import (
    CustomerService,
)
from app.features.customer.dependencies.services.customer import (
    get_customer_service,
)

from app.features.pricing.dependencies.services.sale_pricing_service import (
    get_sale_pricing_service,
)
from app.features.pricing.services.sale_pricing import (
    SalePricingService,
)

from app.features.orders.dependencies.services import (
    get_order_service,
    get_order_item_service,
    get_order_promotion_service,
    get_order_address_service,
    get_order_billing_service,
    get_order_pickup_service,
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

from app.features.orders.use_cases.create_order import (
    CreateOrderUseCase,
)
from app.features.locations.dependencies.services import get_ubigeo_service, get_location_service
from app.features.locations.services.ubigeo_service import UbigeoService
from app.features.inventory.dependencies.services import InventoryMovementService, InventoryService, get_inventory_movement_service, get_inventory_service
from app.features.orders.services.order_pickup_service import OrderPickupService
from app.features.locations.services.location_service import LocationService

def get_create_order_use_case(
    order_service: OrderService = Depends(
        get_order_service
    ),
    order_item_service: OrderItemService = Depends(
        get_order_item_service
    ),
    order_promotion_service: OrderPromotionService = Depends(
        get_order_promotion_service
    ),
    order_address_service: OrderAddressService = Depends(
        get_order_address_service
    ),
    order_billing_service: OrderBillingService = Depends(
        get_order_billing_service
    ),
    customer_service: CustomerService = Depends(
        get_customer_service
    ),
    cart_service: CartService = Depends(
        get_cart_service
    ),
    sale_pricing_service: SalePricingService = Depends(
        get_sale_pricing_service
    ),
    ubigeo_service: UbigeoService = Depends(
        get_ubigeo_service
    ),
    inventory_movement_service: InventoryMovementService = Depends(
        get_inventory_movement_service
    ),
    inventory_service: InventoryService = Depends(
        get_inventory_service
    ),
    order_pickup_service: 
        OrderPickupService =
        Depends(get_order_pickup_service),
    location_service: 
        LocationService =
        Depends(get_location_service),
) -> CreateOrderUseCase:
    return CreateOrderUseCase(
        order_service=order_service,
        order_item_service=order_item_service,
        order_promotion_service=order_promotion_service,
        order_address_service=order_address_service,
        order_billing_service=order_billing_service,
        customer_service=customer_service,
        cart_service=cart_service,
        sale_pricing_service=sale_pricing_service,
        ubigeo_service=ubigeo_service,
        inventory_service=inventory_service,
        inventory_movement_service=inventory_movement_service,
        order_pickup_service=order_pickup_service,
        location_service=location_service,
    )