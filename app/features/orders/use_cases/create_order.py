from datetime import UTC, datetime
from decimal import Decimal

from app.features.locations.services.ubigeo_service import (
    UbigeoService,
)

from app.features.orders.services.order_address_service import OrderAddressService
from app.features.orders.services.order_billing_service import OrderBillingService
from app.features.orders.services.order_item_service import OrderItemService

from app.features.orders.services.order_promotion_service import OrderPromotionService

from app.features.orders.services.order_service import OrderService

from app.features.cart.service import CartService
from app.features.pricing.services.sale_pricing import SalePricingService
from app.features.customer.customer_service import CustomerService
from app.features.orders.types.order import CreateOrderInput, CreateOrderAddressDTO, CreateOrderBillingDTO, CreateOrderResult, CreateOrderItemResult
from app.features.customer.entities.customer import CustomerEntity

from app.features.cart.dto import CartItemRow
from app.features.pricing.dtos.sale_pricing import SalePricingContext, SalePricingDTO, PricingItemDTO
from app.features.orders.entities.order_item import OrderItem
from app.features.orders.entities.order_address import OrderAddress
from app.features.orders.entities.order_billing import OrderBilling
from app.features.orders.entities.order_promotion import OrderPromotion
from app.features.receipts.types.document import BillingDocumentType
from app.features.customer.customer_types import IdentityDocumentType
from app.features.orders.types.sale import SaleChannel

from app.features.inventory.services.inventory_service import InventoryService
from app.features.inventory.services.inventory_movement_service import (
    InventoryMovementService,
)

from app.features.inventory.dtos.inventory import (
    InventoryReservationItem,
    InventoryReservationResult,
)

from app.features.orders.services.order_pickup_service import (
    OrderPickupService,
)
from app.features.orders.types.delivery import DeliveryMethod

from app.features.locations.services.location_service import (
    LocationService,
)


from app.features.inventory.types.inventory_movement import (
    InventoryMovementType,
    InventoryOwnerType,
)

from app.features.inventory.types.inventory_reference import (
    InventoryReferenceType,
)

from app.core.exceptions import ValidationError


class CreateOrderUseCase:

    def __init__(
        self,
        *,
        order_service: OrderService,
        order_item_service: OrderItemService,
        order_promotion_service: OrderPromotionService,
        order_address_service: OrderAddressService,
        order_billing_service: OrderBillingService,
        customer_service: CustomerService,
        cart_service: CartService,
        sale_pricing_service: SalePricingService,
        inventory_service: InventoryService,
        inventory_movement_service: InventoryMovementService,
        ubigeo_service: UbigeoService,
        order_pickup_service: OrderPickupService,
        location_service: LocationService
    ):
        self._order_service = order_service
        self._order_item_service = order_item_service
        self._order_promotion_service = order_promotion_service
        self._order_address_service = order_address_service
        self._order_billing_service = order_billing_service
        self._customer_service = customer_service
        self._cart_service = cart_service
        self._sale_pricing_service = sale_pricing_service
        self._inventory_service = inventory_service
        self._ubigeo_service = ubigeo_service
        self._inventory_movement_service = (
            inventory_movement_service
        )
        self._order_pickup_service = order_pickup_service
        self._location_service = location_service

    async def execute(
        self,
        input: CreateOrderInput,
    ) -> CreateOrderResult:
        now = datetime.now(UTC)

        customer = await self._resolve_customer(
            input=input,
            now=now,
        )

        cart = await self._cart_service.get_cart_by_owner(
            user_id=input.user_id,
            session_id=input.session_id,
        )

        cart_items = await self._cart_service.get_cart_items(
            cart_id=cart.id,
        )

        if not cart_items:
            raise ValidationError(
                message="El carrito no puede estar vacio al momento de crear el pedido.",
                context={
                    "user_id": input.user_id,
                    "session_id": input.session_id,
                },
            )

        
        pickup_location = None

        if input.delivery_method == DeliveryMethod.STORE_PICKUP:
            if input.pickup is None or input.address is not None:
                raise ValidationError(
                    message="Los datos de recojo no son válidos."
                )

            pickup_location = await self._location_service.get_pickup_location(
                location_id=input.pickup.location_id,
            )

            base_shipping_cost = Decimal("0.00")

        elif input.delivery_method == DeliveryMethod.SHIPPING:
            if input.address is None or input.pickup is not None:
                raise ValidationError(
                    message="Los datos de envío no son válidos."
                )

            base_shipping_cost = await self._resolve_shipping_cost(
                ubigeo_code=input.address.ubigeo_code,
            )

        else:
            raise ValidationError(
                message="Método de entrega no soportado."
            )


        pricing = await self._calculate_pricing(
            input=input,
            customer=customer,
            cart_items=cart_items,
            base_shipping_cost=base_shipping_cost,
            now=now,
        )

        order = await self._order_service.create(
            customer_id=customer.id,
            subtotal=pricing.subtotal,
            payment_method=input.payment_method,
            discount_amount=pricing.discount_amount,
            delivery_method=input.delivery_method,
            shipping_cost=pricing.shipping_cost,
            total=pricing.total,
            now=now,
        )

        created_items = await self._create_items(
            order_id=order.id,
            cart_items=cart_items,
            pricing=pricing,
        )

        reservations = await (
            self._reserve_inventory(
                cart_items=cart_items,
            )
        )

        await self._create_reservation_movements(
            order_id=order.id,
            order_number=order.order_number,
            cart_items=cart_items,
            reservations=reservations,
        )

        await self._create_promotions(
            order_id=order.id,
            pricing=pricing,
        )

        if input.delivery_method == DeliveryMethod.SHIPPING:
            await self._create_address(
                order_id=order.id,
                address=input.address,
            )
        else:
            
            await self._order_pickup_service.create(
                order_id=order.id,
                location_id=pickup_location.id,
                location_name=pickup_location.name,
                location_address=pickup_location.address,
                location_ubigeo_code=pickup_location.ubigeo_code,
                location_latitude=pickup_location.latitude,
                location_longitude=pickup_location.longitude,
                location_phone=pickup_location.phone,
                location_reference=pickup_location.reference,
                created_at=now,
            )

        if input.billing is not None:
            await self._create_billing(
                order_id=order.id,
                customer=customer,
                billing=input.billing,
            )

        await self._cart_service.clear_cart(
            cart_id=cart.id,
        )

        return CreateOrderResult(
            id=order.id,
            order_number=order.order_number,
            status=order.status,
            subtotal=order.subtotal,
            discount_amount=order.discount_amount,
            shipping_cost=order.shipping_cost,
            total=order.total,
            items=[
                CreateOrderItemResult(
                    product_name=item.product_name,
                    color=item.color,
                    size=item.size,
                    quantity=item.quantity,
                    final_total=item.final_total,
                )
                for item in created_items
            ],
        )


    async def _create_reservation_movements(
        self,
        *,
        order_id: int,
        order_number: str,
        cart_items: list[CartItemRow],
        reservations: list[
            InventoryReservationResult
        ],
    ) -> None:

        items_by_owner = {
            item.variant_size_id: item
            for item in cart_items
        }

        for reservation in reservations:

            item = items_by_owner[
                reservation.owner_id
            ]

            await (
                self._inventory_movement_service
                .create_movement(
                    movement_type=(
                        InventoryMovementType
                        .RESERVATION
                    ),

                    owner_type=(
                        InventoryOwnerType
                        .PRODUCT
                    ),

                    owner_id=(
                        reservation.owner_id
                    ),

                    location_id=(
                        reservation.location_id
                    ),

                    owner_name=(
                        item.nombre
                    ),

                    owner_code=(
                        item.sku
                    ),

                    quantity=(
                        reservation.quantity
                    ),

                    prev_stock=(
                        reservation
                        .stock_quantity
                    ),

                    new_stock=(
                        reservation
                        .stock_quantity
                    ),

                    reference_type=(
                        InventoryReferenceType
                        .ORDER
                    ),

                    reference_id=(
                        order_id
                    ),

                    reason=(
                        f"Reserva automática del "
                        f"pedido {order_number}. "
                        f"Se reservaron "
                        f"{reservation.quantity} "
                        f"unidad(es). "
                        f"Disponible: "
                        f"{reservation.previous_available_quantity} "
                        f"→ "
                        f"{reservation.current_available_quantity}."
                    ),
                )
            )

    async def _reserve_inventory(
        self,
        *,
        cart_items: list[CartItemRow],
    ) -> list[InventoryReservationResult]:

        items = [
            InventoryReservationItem(
                owner_id=(
                    item.variant_size_id
                ),
                quantity=Decimal(
                    item.quantity
                ),
            )
            for item in cart_items
        ]

        return await (
            self._inventory_service
            .reserve_stock_many(
                owner_type=(
                    InventoryOwnerType.PRODUCT
                ),
                items=items,
            )
        )

    async def _resolve_customer(
        self,
        *,
        input: CreateOrderInput,
        now: datetime
    ) -> CustomerEntity:
        if input.user_id is not None:
            customer = await self._customer_service.get_by_user_id(
                input.user_id
            )
        else:
            customer = await self._customer_service.get_by_session_id(
                input.session_id
            )

        if customer is not None:
            return customer

        if input.customer is None:
            raise ValidationError(
                message="Los datos de cliente son obligatorios para registrarlo.",
                context={
                    "user_id": input.user_id,
                    "session_id": input.session_id,
                },
            )

        return await self._customer_service.create(
            user_id=input.user_id,
            session_id=input.session_id,
            name=input.customer.name,
            last_name=input.customer.last_name,
            email=input.customer.email,
            phone=input.customer.phone,
            created_at=now,
            updated_at=now
        )

    async def _calculate_pricing(
        self,
        *,
        input: CreateOrderInput,
        customer: CustomerEntity,
        cart_items: list[CartItemRow],
        base_shipping_cost: Decimal,
        now: datetime,
    ) -> SalePricingDTO:
        
        context = SalePricingContext(
            items=[
                PricingItemDTO(
                    item_id=item.cart_item_id,
                    product_id=item.product_id,
                    category=item.category,
                    brand=item.brand,
                    quantity=item.quantity,
                    unit_price=item.base_price
                )
                for item in cart_items
            ],
            customer_id=customer.id,
            sale_channel=SaleChannel.ECOMMERCE,
            customer_type=customer.customer_type,
            shipping_cost=base_shipping_cost,
            coupon_code=input.coupon_code,
            payment_method=input.payment_method,
            now=now,
        )

        return await self._sale_pricing_service.calculate(context=context)

    async def _resolve_shipping_cost(
        self,
        *,
        ubigeo_code: str,
    ) -> Decimal:
        ubigeo = await self._ubigeo_service.get_by_code(
            ubigeo_code
        )

        if ubigeo is None:
            raise ValidationError(
                message="El ubigeo indicado no existe.",
                context={
                    "ubigeo_code": ubigeo_code,
                },
            )

        if ubigeo.department.upper() == "LIMA":
            return Decimal("10.00")

        return Decimal("12.00")

    async def _create_items(
        self,
        *,
        order_id: int,
        cart_items: list[CartItemRow],
        pricing: SalePricingDTO,
    ) -> list[OrderItem]:

        pricing_by_item_id = {
            item.item_id: item
            for item in pricing.items
        }

        items = []

        for cart_item in cart_items:
            priced_item = pricing_by_item_id[cart_item.cart_item_id]

            items.append(
                OrderItem(
                    order_id=order_id,

                    product_id=cart_item.product_id,
                    variant_id=cart_item.variant_id,
                    variant_size_id=cart_item.variant_size_id,

                    product_name=cart_item.nombre,
                    sku=cart_item.sku,
                    color=cart_item.color,
                    size=cart_item.size,

                    quantity=cart_item.quantity,

                    unit_original_price=priced_item.original_unit_price,
                    unit_final_price=priced_item.final_unit_price,

                    original_total=priced_item.original_total,
                    discount_amount=priced_item.discount_amount,
                    final_total=priced_item.final_total,
                )
            )

        await self._order_item_service.create_all(items)

        return items

    async def _create_promotions(
        self,
        *,
        order_id: int,
        pricing: SalePricingDTO,
    ) -> None:

        promotions = [
            OrderPromotion(
                order_id=order_id,
                promotion_id=promotion.promotion_id,
                name=promotion.name,
                application_scope=promotion.application_scope,
                coupon_code=promotion.coupon_code,
                discount_amount=promotion.discount_amount,
            )
            for promotion in pricing.applied_promotions
        ]

        await self._order_promotion_service.create_all(promotions)

    async def _create_address(
        self,
        *,
        order_id: int,
        address: CreateOrderAddressDTO,
    ) -> None:
        await self._order_address_service.create(
            OrderAddress(
                order_id=order_id,
                recipient_name=address.recipient_name,
                phone=address.phone,
                address=address.address,
                latitude=address.latitude,
                ubigeo_code=address.ubigeo_code,
                longitude=address.longitude,
                reference=address.reference,
                delivery_instructions=address.delivery_instructions,
            )
        )

    async def _create_billing(
        self,
        *,
        order_id: int,
        customer: CustomerEntity,
        billing: CreateOrderBillingDTO,
    ) -> None:

        if billing.document_type == BillingDocumentType.INVOICE:
            if not billing.business_name:
                raise ValidationError(
                    message="El nombre de empresa es obligatorio al emitir factura.",
                    context={
                        "document_type": billing.document_type.value,
                    },
                )

            recipient_name = billing.business_name
            identity_document_type = IdentityDocumentType.RUC

        else:
            recipient_name = (
                f"{customer.name} {customer.last_name}"
            ).strip()

            identity_document_type = IdentityDocumentType.DNI

        await self._order_billing_service.create(
            OrderBilling(
                order_id=order_id,
                document_type=billing.document_type,
                identity_document_type=identity_document_type,
                identity_document_number=billing.identity_document_number,
                recipient_name=recipient_name,
                email=customer.email,
                billing_address=billing.billing_address,
            )
        )