# app/infra/db/uow/repositories/orders.py

from app.features.orders.repositories.order_repository import (
    OrderRepository,
)
from app.features.orders.models.order import (
    OrderTable,
)
from app.features.orders.mappers.order import (
    OrderMapper,
)

from app.features.orders.repositories.order_item_repository import (
    OrderItemRepository,
)
from app.features.orders.models.order_item import (
    OrderItemTable,
)
from app.features.orders.mappers.order_item import (
    OrderItemMapper,
)

from app.features.orders.repositories.order_promotion_repository import (
    OrderPromotionRepository,
)
from app.features.orders.models.order_promotion import (
    OrderPromotionTable,
)
from app.features.orders.mappers.order_promotion import (
    OrderPromotionMapper,
)

from app.features.orders.repositories.order_address_repository import (
    OrderAddressRepository,
)
from app.features.orders.models.order_address import (
    OrderAddressTable,
)
from app.features.orders.mappers.order_address import (
    OrderAddressMapper,
)

from app.features.orders.repositories.order_billing_repository import (
    OrderBillingRepository,
)
from app.features.orders.models.order_billing import (
    OrderBillingTable,
)
from app.features.orders.mappers.order_billing import (
    OrderBillingMapper,
)

from app.features.locations.mappers.ubigeo_mapper import (
    UbigeoMapper,
)
from app.features.locations.models.ubigeo import (
    UbigeoTable,
)
from app.features.locations.repositories.ubigeo_repository import (
    UbigeoRepository,
)
from app.features.orders.repositories.order_receipt_repository import (
    OrderReceiptRepository,
)
from app.features.orders.models.order_receipt import (
    OrderReceiptTable,
)
from app.features.orders.mappers.order_receipt import (
    OrderReceiptMapper,
)

from app.features.orders.mappers.order_pickup_mapper import (
    OrderPickupMapper,
)
from app.features.orders.models.order_pickup import (
    OrderPickupTable,
)
from app.features.orders.repositories.order_pickup_repository import (
    OrderPickupRepository,
)

from app.features.locations.mappers.location_mapper import (
    LocationMapper,
)
from app.features.locations.models.locations import LocationTable
from app.features.locations.repositories.location_repository import (
    LocationRepository,
)

class OrdersRepositoriesMixin:

    @property
    def locations(self) -> LocationRepository:
        return self._get_or_create(
            "locations",
            lambda: LocationRepository(
                self.session,
                LocationMapper,
                LocationTable,
            ),
        )

    @property
    def order_pickups(self) -> OrderPickupRepository:
        return self._get_or_create(
            "order_pickups",
            lambda: OrderPickupRepository(
                self.session,
                OrderPickupMapper,
                OrderPickupTable,
            ),
        )

    @property
    def order_receipts(
        self,
    ) -> OrderReceiptRepository:
        return self._get_or_create(
            "order_receipts",
            lambda: OrderReceiptRepository(
                self.session,
                OrderReceiptMapper,
                OrderReceiptTable,
            ),
        )

    @property
    def ubigeos(
        self,
    ) -> UbigeoRepository:
        return self._get_or_create(
            "ubigeos",
            lambda: UbigeoRepository(
                self.session,
                UbigeoMapper,
                UbigeoTable,
            ),
        )

    @property
    def orders(
        self,
    ) -> OrderRepository:
        return self._get_or_create(
            "orders",
            lambda: OrderRepository(
                self.session,
                OrderMapper,
                OrderTable,
            ),
        )

    @property
    def order_items(
        self,
    ) -> OrderItemRepository:
        return self._get_or_create(
            "order_items",
            lambda: OrderItemRepository(
                self.session,
                OrderItemMapper,
                OrderItemTable,
            ),
        )

    @property
    def order_promotions(
        self,
    ) -> OrderPromotionRepository:
        return self._get_or_create(
            "order_promotions",
            lambda: OrderPromotionRepository(
                self.session,
                OrderPromotionMapper,
                OrderPromotionTable,
            ),
        )

    @property
    def order_addresses(
        self,
    ) -> OrderAddressRepository:
        return self._get_or_create(
            "order_addresses",
            lambda: OrderAddressRepository(
                self.session,
                OrderAddressMapper,
                OrderAddressTable,
            ),
        )

    @property
    def order_billings(
        self,
    ) -> OrderBillingRepository:
        return self._get_or_create(
            "order_billings",
            lambda: OrderBillingRepository(
                self.session,
                OrderBillingMapper,
                OrderBillingTable,
            ),
        )