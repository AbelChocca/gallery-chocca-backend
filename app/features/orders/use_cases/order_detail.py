from app.features.orders.types.order import (
    AdminOrderAddressDTO,
    AdminOrderBillingDTO,
    AdminOrderCustomerDTO,
    AdminOrderDetailDTO,
    AdminOrderItemDTO,
    AdminOrderPromotionDTO,
    AdminOrderReceiptDTO,
    OrderPickupDetailDTO
)

from app.features.orders.services.order_service import (
    OrderService,
)

from app.features.orders.services.order_item_service import (
    OrderItemService,
)
from app.features.orders.services.order_receipt import (
    OrderReceiptService,
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

from app.features.customer.customer_service import (
    CustomerService,
)
from app.features.locations.services.ubigeo_service import UbigeoService

from app.core.exceptions import (
    ValueNotFound,
)
from app.features.orders.services.order_pickup_service import (
    OrderPickupService,
)

from app.features.locations.services.location_service import (
    LocationService,
)

from app.features.orders.types.delivery import DeliveryMethod


class GetAdminOrderDetailUseCase:

    def __init__(
        self,
        *,
        order_service: OrderService,
        order_item_service: OrderItemService,
        order_promotion_service: OrderPromotionService,
        order_address_service: OrderAddressService,
        order_billing_service: OrderBillingService,
        order_receipt_service: OrderReceiptService,
        customer_service: CustomerService,
        ubigeo_service: UbigeoService,
        order_pickup_service: OrderPickupService,
        location_service: LocationService,
    ) -> None:
        self._order_service = order_service
        self._order_item_service = order_item_service
        self._order_promotion_service = order_promotion_service
        self._order_address_service = order_address_service
        self._order_billing_service = order_billing_service
        self._order_receipt_service = (
            order_receipt_service
        )
        self._order_pickup_service = order_pickup_service
        self._location_service = location_service
        self._customer_service = customer_service
        self._ubigeo_service = ubigeo_service

    async def execute(
        self,
        order_id: int,
    ) -> AdminOrderDetailDTO:

        order = await self._order_service.get_by_id(
            order_id
        )

        if order is None:
            raise ValueNotFound(
                "No fue posible encontrar el pedido, reintentalo.",
                context={
                    "order_id": order_id,
                },
            )

        if order.customer_id is None:
            raise ValueNotFound(
                "Cliente asociado al pedido no fue encontrado.",
                context={
                    "order_id": order_id,
                },
            )

        customer = await self._customer_service.get_by_id(
            order.customer_id
        )

        if customer is None:
            raise ValueNotFound(
                "Cliente asociado al pedido no fue encontrado.",
                context={
                    "order_id": order_id,
                    "customer_id": order.customer_id,
                },
            )

        items = await self._order_item_service.get_by_order_id(
            order.id
        )

        promotions = (
            await self._order_promotion_service.get_by_order_id(
                order.id
            )
        )

        address_dto: AdminOrderAddressDTO | None = None
        pickup_dto: OrderPickupDetailDTO | None = None

        if order.delivery_method == DeliveryMethod.SHIPPING:
            address = await self._order_address_service.get_by_order_id(
                order.id
            )

            ubigeo = await self._ubigeo_service.get_by_code(
                address.ubigeo_code
            )

            if ubigeo is None:
                raise ValueNotFound(
                    "El ubigeo asociado al pedido no fue encontrado.",
                    context={
                        "order_id": order.id,
                        "ubigeo_code": address.ubigeo_code,
                    },
                )

            address_dto = AdminOrderAddressDTO(
                recipient_name=address.recipient_name,
                phone=address.phone,
                ubigeo_code=address.ubigeo_code,
                department=ubigeo.department,
                province=ubigeo.province,
                district=ubigeo.district,
                city_name=ubigeo.city_name,
                address=address.address,
                latitude=address.latitude,
                longitude=address.longitude,
                reference=address.reference,
                delivery_instructions=address.delivery_instructions,
            )

        elif order.delivery_method == DeliveryMethod.STORE_PICKUP:
            pickup = await self._order_pickup_service.get_by_order_id(
                order_id=order.id
            )

            location = await self._location_service.get_by_id(
                location_id=pickup.location_id
            )

            if location is None:
                raise ValueNotFound(
                    "La tienda de recojo asociada al pedido no existe.",
                    context={
                        "order_id": order.id,
                        "location_id": pickup.location_id,
                    },
                )

            pickup_dto = OrderPickupDetailDTO(
                location_id=location.id,
                name=location.name,
                address=location.address,
            )

        else:
            raise ValueError(
                f"Modalidad de entrega no soportada: {order.delivery_method}"
            )

        billing = (
            await self._order_billing_service.get_by_order_id(
                order.id
            )
        )

        order_receipt = (
            await self._order_receipt_service
            .get_by_order_id(
                order_id=order.id,
                raises=False,
            )
        )

        return AdminOrderDetailDTO(
            id=order.id,
            order_number=order.order_number,

            status=order.status,

            subtotal=order.subtotal,
            discount_amount=order.discount_amount,
            shipping_cost=order.shipping_cost,
            total=order.total,

            customer=AdminOrderCustomerDTO(
                id=customer.id,
                name=customer.name,
                last_name=customer.last_name,
                document_type=customer.document_type,
                document_number=customer.document_number,
                email=customer.email,
                phone=customer.phone,
            ),
            receipt=(
                AdminOrderReceiptDTO(
                status=order_receipt.status,

                external_id=(
                    order_receipt.external_id
                ),

                series_number=(
                    order_receipt.series_number
                ),

                provider_error_code=(
                    order_receipt.provider_error_code
                ),

                provider_error_message=(
                    order_receipt.provider_error_message
                ),

                issued_at=(
                    order_receipt.issued_at
                ),

                email_provider_id=(
                    order_receipt.email_provider_id
                ),

                email_sent_at=(
                    order_receipt.email_sent_at
                ),

                email_error_message=(
                    order_receipt.email_error_message
                ),
            )
            if order_receipt is not None
            else None
            ),

            items=[
                AdminOrderItemDTO(
                    id=item.id,

                    product_id=item.product_id,
                    variant_id=item.variant_id,
                    variant_size_id=item.variant_size_id,

                    product_name=item.product_name,
                    sku=item.sku,

                    color=item.color,
                    size=item.size,

                    quantity=item.quantity,

                    unit_original_price=item.unit_original_price,
                    unit_final_price=item.unit_final_price,

                    discount_amount=item.discount_amount,

                    original_total=item.original_total,
                    final_total=item.final_total,
                )
                for item in items
            ],

            promotions=[
                AdminOrderPromotionDTO(
                    id=promotion.id,

                    promotion_id=promotion.promotion_id,

                    name=promotion.name,

                    application_scope=promotion.application_scope,

                    coupon_code=promotion.coupon_code,

                    discount_amount=promotion.discount_amount,
                )
                for promotion in promotions
            ],

            delivery_method=order.delivery_method,

            address=address_dto,
            pickup=pickup_dto,

            billing=(
                AdminOrderBillingDTO(
                    document_type=billing.document_type,

                    identity_document_type=(
                        billing.identity_document_type
                    ),

                    identity_document_number=(
                        billing.identity_document_number
                    ),

                    recipient_name=billing.recipient_name,

                    email=billing.email,

                    billing_address=billing.billing_address,
                )
                if billing is not None
                else None
            ),

            created_at=order.created_at,
            updated_at=order.updated_at,
        )