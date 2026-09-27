from datetime import datetime, timezone
from decimal import Decimal

from app.features.cart.dto import (
    CartItemDTO,
    FullCartDTO,
    CartItemRow
)
from app.features.cart.service import (
    CartService,
)
from app.features.sales.types.customer import (
    CustomerType,
)
from app.features.pricing.dtos.cart_pricing_dto import (
    CartPricingContext,
    CartPricingItemDTO,
    CartPricingItemResultDTO,
)
from app.features.pricing.services.cart_pricing import (
    CartPricingService,
)
from app.features.sales.types.sale import (
    SaleChannel,
)


class GetFullCartUseCase:

    def __init__(
        self,
        *,
        cart_service: CartService,
        cart_pricing_service: CartPricingService,
    ) -> None:
        self._cart_service = cart_service
        self._cart_pricing_service = (
            cart_pricing_service
        )

    async def execute(
        self,
        *,
        user_id: int | None,
        session_id: str | None,
        customer_id: int | None,
        customer_type: CustomerType | None,
    ) -> FullCartDTO | None:
        cart = await self._cart_service.get_cart_by_owner(
            user_id=user_id,
            session_id=session_id,
        )

        if cart is None:
            return None

        items = await self._cart_service.get_cart_items(
            cart_id=cart.id,
        )

        if not items:
            return self._empty_cart(
                cart_id=cart.id,
            )

        pricing_context = (
            self._build_pricing_context(
                items=items,
                customer_id=customer_id,
                customer_type=customer_type,
            )
        )

        pricing = (
            await self._cart_pricing_service.calculate(
                context=pricing_context,
            )
        )

        pricing_by_item = {
            item.item_id: item
            for item in pricing.items
        }

        parsed_items = self._build_items(
            items=items,
            pricing_by_item=pricing_by_item,
        )

        return FullCartDTO(
            cart_id=cart.id,
            items=parsed_items,
            subtotal=pricing.subtotal,
            discount_amount=pricing.discount_amount,
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
    ) -> CartPricingContext:
        return CartPricingContext(
            items=[
                CartPricingItemDTO(
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
            now=datetime.now(timezone.utc),
        )

    def _build_items(
        self,
        *,
        items: list[CartItemRow],
        pricing_by_item: dict[
            int,
            CartPricingItemResultDTO,
        ],
    ) -> list[CartItemDTO]:
        result: list[CartItemDTO] = []

        for item in items:
            pricing = pricing_by_item[
                item.cart_item_id
            ]

            result.append(
                CartItemDTO(
                    cart_item_id=item.cart_item_id,

                    product_id=item.product_id,
                    nombre=item.nombre,

                    variant_id=item.variant_id,
                    color=item.color,

                    variant_size_id=item.variant_size_id,
                    size=item.size,
                    sku=item.sku,

                    quantity=item.quantity,
                    stock=item.stock,
                    has_stock=item.has_stock,
                    is_product_active=(
                        item.is_product_active
                    ),

                    image_url=item.image_url,

                    original_price=(
                        pricing.original_unit_price
                    ),
                    final_price=(
                        pricing.final_unit_price
                    ),
                    discount_amount=(
                        pricing.discount_amount
                    ),
                    has_discount=(
                        pricing.has_discount
                    ),

                    original_total=(
                        pricing.original_total
                    ),
                    final_total=(
                        pricing.final_total
                    ),
                    applied_promotions=(
                        pricing.applied_promotions
                    ),
                )
            )

        return result

    def _empty_cart(
        self,
        *,
        cart_id: int,
    ) -> FullCartDTO:
        zero = Decimal("0.00")

        return FullCartDTO(
            cart_id=cart_id,
            items=[],
            subtotal=zero,
            discount_amount=zero,
            total=zero,
            total_items=0,
        )