from decimal import Decimal

from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.calculators.calculator_dto import PricingItemCalculationResult

from app.features.pricing.dtos.cart_pricing_dto import AppliedPromotionDTO

class PricingItemCalculator:

    def calculate(
        self,
        *,
        unit_price: Decimal,
        quantity: int,
        promotions: list[Promotion],
        shipping_cost: Decimal = Decimal("0.00"),
    ) -> PricingItemCalculationResult:

        original_unit_price = unit_price
        current_unit_price = unit_price
        current_shipping_cost = shipping_cost
        discount_amount = Decimal("0.00")

        applied_promotions: list[AppliedPromotionDTO] = []

        for promotion in promotions:
            promotion_discount_amount = Decimal("0.00")

            for rule in promotion.pricing_rules:
                result = rule.apply(
                    current_price=current_unit_price,
                    quantity=quantity,
                    shipping_cost=current_shipping_cost,
                )

                current_unit_price = result.unit_price
                current_shipping_cost = result.shipping_cost

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

        return PricingItemCalculationResult(
            original_unit_price=original_unit_price,
            final_unit_price=current_unit_price,
            original_total=original_unit_price * quantity,
            final_total=current_unit_price * quantity,
            discount_amount=discount_amount,
            shipping_cost=current_shipping_cost,
            applied_promotions=applied_promotions,
        )

def get_pricing_item_calculator() -> PricingItemCalculator:
    return PricingItemCalculator()