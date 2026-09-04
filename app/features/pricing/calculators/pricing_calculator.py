from decimal import Decimal

from app.features.pricing.dtos.sale_pricing import (
    PricingItemResultDTO,
    SalePricingDTO,
)
from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.dtos.sale_pricing import SalePricingContext


class PricingCalculator:

    def calculate(
        self,
        *,
        context: SalePricingContext,
        promotions_by_product: dict[int, list[Promotion]],
    ) -> SalePricingDTO:

        results: list[PricingItemResultDTO] = []

        subtotal = Decimal("0.00")
        discount_amount = Decimal("0.00")

        shipping_cost = context.shipping_cost

        for item in context.items:

            original_unit_price = item.unit_price

            current_unit_price = item.unit_price
            item_discount = Decimal("0.00")

            promotions = promotions_by_product.get(
                item.product_id,
                [],
            )

            for promotion in promotions:

                for rule in promotion.pricing_rules:

                    result = rule.strategy.apply(
                        current_price=current_unit_price,
                        quantity=item.quantity,
                        parameters=rule.parameters,
                        shipping_cost=shipping_cost,
                    )

                    current_unit_price = result.unit_price

                    shipping_cost = result.shipping_cost

                    item_discount += result.discount_amount

            original_total = (
                original_unit_price * item.quantity
            )

            final_total = (
                current_unit_price * item.quantity
            )

            subtotal += original_total

            discount_amount += item_discount

            results.append(
                PricingItemResultDTO(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    original_unit_price=original_unit_price,
                    final_unit_price=current_unit_price,
                    original_total=original_total,
                    final_total=final_total,
                    discount_amount=item_discount,
                )
            )

        total = (
            subtotal
            - discount_amount
            + shipping_cost
        )

        return SalePricingDTO(
            items=results,
            subtotal=subtotal,
            discount_amount=discount_amount,
            shipping_cost=shipping_cost,
            total=total,
        )