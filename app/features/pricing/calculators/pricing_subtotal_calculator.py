from decimal import Decimal

from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.calculators.calculator_dto import (
    PricingSubtotalCalculationResult,
)
from app.features.pricing.dtos.cart_pricing_dto import AppliedPromotionDTO


class PricingSubtotalCalculator:

    def calculate(
        self,
        *,
        subtotal: Decimal,
        promotions: list[Promotion],
    ) -> PricingSubtotalCalculationResult:

        current_subtotal = subtotal
        discount_amount = Decimal("0.00")

        applied_promotions: list[AppliedPromotionDTO] = []

        for promotion in promotions:
            promotion_discount_amount = Decimal("0.00")

            for rule in promotion.pricing_rules:
                result = rule.apply(
                    current_price=current_subtotal,
                    quantity=1,
                    shipping_cost=Decimal("0.00"),
                )

                current_subtotal = result.unit_price

                promotion_discount_amount += result.discount_amount
                discount_amount += result.discount_amount

            if promotion_discount_amount > 0:
                applied_promotions.append(
                    AppliedPromotionDTO(
                        promotion_id=promotion.id,
                        name=promotion.name,
                        discount_amount=promotion_discount_amount,
                    )
                )

        return PricingSubtotalCalculationResult(
            original_subtotal=subtotal,
            final_subtotal=current_subtotal,
            discount_amount=discount_amount,
            applied_promotions=applied_promotions,
        )


def get_pricing_subtotal_calculator() -> PricingSubtotalCalculator:
    return PricingSubtotalCalculator()