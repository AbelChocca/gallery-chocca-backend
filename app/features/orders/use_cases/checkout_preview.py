from datetime import datetime
from decimal import Decimal

from app.features.cart.dto import CartItemRow
from app.features.cart.service import CartService

from app.features.orders.types.order import (
    CheckoutItemDTO,
    CheckoutPreviewDTO,
)

from app.features.pricing.dtos.sale_pricing import (
    SalePricingContext,
    PricingItemResultDTO,
    PricingItemDTO
)
from app.features.pricing.services.sale_pricing import (
    SalePricingService,
)

from app.features.customer.customer_types import CustomerType
from app.features.payments.types.payment_legacy import PaymentMethod
from app.features.orders.types.sale import SaleChannel
from app.features.orders.types.shipping import ShippingLocationDTO
from app.features.locations.services.ubigeo_service import UbigeoService
from app.features.locations.services.location_service import LocationService
from app.features.orders.types.delivery import DeliveryMethod

from app.core.exceptions import ValidationError

class CheckoutPreviewUseCase:

    def __init__(
        self,
        *,
        cart_service: CartService,
        sale_pricing_service: SalePricingService,
        ubigeo_service: UbigeoService,
        location_service: LocationService,
    ) -> None:
        self._cart_service = cart_service
        self._sale_pricing_service = sale_pricing_service
        self._ubigeo_service = ubigeo_service
        self._location_service = location_service

    async def execute(
        self,
        *,
        user_id: int | None,
        session_id: str | None,
        customer_id: int | None,
        customer_type: CustomerType | None,
        coupon_code: str | None,
        payment_method: PaymentMethod | None,
        shipping_location: ShippingLocationDTO | None,
        delivery_method: DeliveryMethod,
        pickup_location_id: int | None,
        now: datetime,
    ) -> CheckoutPreviewDTO | None:
        cart_id = await self._cart_service.get_cart_id_by_owner(
            user_id=user_id,
            session_id=session_id,
        )

        if cart_id is None:
            return None

        items = await self._cart_service.get_cart_items(
            cart_id=cart_id,
        )

        if not items:
            return self._empty_checkout(
                cart_id=cart_id,
            )

        shipping_cost = await self._calculate_shipping_cost(
            delivery_method=delivery_method,
            shipping_location=shipping_location,
            pickup_location_id=pickup_location_id,
        )

        pricing_context = self._build_pricing_context(
            items=items,
            customer_id=customer_id,
            customer_type=customer_type,
            coupon_code=coupon_code,
            payment_method=payment_method,
            shipping_cost=shipping_cost,
            now=now,
        )

        pricing = await self._sale_pricing_service.calculate(
            context=pricing_context,
        )

        pricing_by_item = {
            item.item_id: item
            for item in pricing.items
        }

        parsed_items = self._build_items(
            items=items,
            pricing_by_item=pricing_by_item,
        )

        return CheckoutPreviewDTO(
            cart_id=cart_id,
            items=parsed_items,
            subtotal=pricing.subtotal,
            discount_amount=pricing.discount_amount,
            shipping_cost=shipping_cost,
            total=pricing.total,
            total_items=sum(
                item.quantity
                for item in items
            ),
            applied_promotions=pricing.applied_promotions,
        )

    def _build_pricing_context(
        self,
        *,
        items: list[CartItemRow],
        customer_id: int | None,
        customer_type: CustomerType | None,
        coupon_code: str | None,
        payment_method: PaymentMethod | None,
        shipping_cost: Decimal,
        now: datetime,
    ) -> SalePricingContext:
        return SalePricingContext(
            items=[
                PricingItemDTO(
                    item_id=item.cart_item_id,
                    product_id=item.product_id,
                    category=item.category,
                    brand=item.brand,
                    quantity=item.quantity,
                    unit_price=item.base_price,
                )
                for item in items
            ],
            sale_channel=SaleChannel.ECOMMERCE,
            customer_id=customer_id,
            customer_type=customer_type,
            coupon_code=coupon_code,
            payment_method=payment_method,
            shipping_cost=shipping_cost,
            now=now,
        )

    def _build_items(
        self,
        *,
        items: list[CartItemRow],
        pricing_by_item: dict[
            int,
            PricingItemResultDTO,
        ],
    ) -> list[CheckoutItemDTO]:
        result: list[CheckoutItemDTO] = []

        for item in items:
            pricing = pricing_by_item[
                item.cart_item_id
            ]

            result.append(
                CheckoutItemDTO(
                    product_id=item.product_id,
                    name=item.nombre,

                    variant_id=item.variant_id,
                    color=item.color,

                    variant_size_id=item.variant_size_id,
                    size=item.size,
                    sku=item.sku,

                    quantity=item.quantity,
                    image_url=item.image_url,

                    original_price=(
                        pricing.original_unit_price
                    ),
                    final_price=(
                        pricing.final_unit_price
                    ),

                    original_total=(
                        pricing.original_total
                    ),
                    discount_amount=(
                        pricing.discount_amount
                    ),
                    final_total=(
                        pricing.final_total
                    ),
                    applied_promotions=pricing.applied_promotions
                )
            )

        return result

    async def _calculate_shipping_cost(
        self,
        *,
        delivery_method: DeliveryMethod,
        shipping_location: ShippingLocationDTO | None,
        pickup_location_id: int | None,
    ) -> Decimal:

        if delivery_method == DeliveryMethod.STORE_PICKUP:
            if pickup_location_id is None or pickup_location_id <= 0:
                raise ValidationError(
                    message="Selecciona una tienda de recojo válida."
                )

            if shipping_location is not None:
                raise ValidationError(
                    message="El recojo en tienda no permite dirección de envío."
                )

            await self._location_service.get_pickup_location(
                location_id=pickup_location_id,
            )

            return Decimal("0.00")

        if delivery_method == DeliveryMethod.SHIPPING:
            if pickup_location_id is not None:
                raise ValidationError(
                    message="El envío a domicilio no permite tienda de recojo."
                )

            if shipping_location is None:
                return Decimal("0.00")

            return await self._resolve_shipping_cost(
                ubigeo_code=shipping_location.ubigeo_code,
            )

        raise ValidationError(
            message="Método de entrega no válido.",
            context={
                "delivery_method": str(delivery_method),
            },
        )

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

        if ubigeo.department.upper() in {
            "LIMA",
            "CALLAO",
        }:
            return Decimal("10.00")

        return Decimal("12.00")

    @staticmethod
    def _empty_checkout(
        *,
        cart_id: int,
    ) -> CheckoutPreviewDTO:
        zero = Decimal("0.00")

        return CheckoutPreviewDTO(
            cart_id=cart_id,
            items=[],
            subtotal=zero,
            discount_amount=zero,
            shipping_cost=zero,
            total=zero,
            total_items=0,
            applied_promotions=[],
        )