from decimal import Decimal
from app.features.pricing.entities.product_applied_pricing_rule import ProductAppliedPricingRule
from app.features.pricing.utils.calculator_dto import PricingCalculationResult

class ProductPricingCalculator:

    def calculate(
        self,
        *,
        base_price: Decimal,
        rules: list[ProductAppliedPricingRule]
    ) -> PricingCalculationResult:

        active_rules = [
            r for r in rules
            if r.pricing_rule.is_active
        ]

        if not active_rules:
            return PricingCalculationResult(
                final_price=base_price.quantize(Decimal("0.01")),
                applied_rules=[],
                latest_applied_rule=None
            )

        stackable_rules: list[ProductAppliedPricingRule] = []
        non_stackable_rules: list[ProductAppliedPricingRule] = []

        # ==========================================
        # SPLIT RULES
        # ==========================================

        for rule in active_rules:
            if rule.pricing_rule.is_stackable:
                stackable_rules.append(rule)
            else:
                non_stackable_rules.append(rule)

        applied = []

        # ==========================================
        # NON STACKABLE DOMINATES
        # ==========================================

        if non_stackable_rules:

            selected_non_stackable = sorted(
                non_stackable_rules,
                key=lambda r: (
                    -r.pricing_rule.priority,
                    -r.assigned_at.timestamp()
                )
            )[0]

            final_price = selected_non_stackable.pricing_rule.apply(
                current_price=base_price
            )

            applied.append(selected_non_stackable)

            return PricingCalculationResult(
                final_price=final_price.quantize(Decimal("0.01")),
                applied_rules=applied,
                latest_applied_rule=selected_non_stackable
            )

        # ==========================================
        # APPLY STACKABLES
        # ==========================================

        final_price = base_price

        stackable_rules = sorted(
            stackable_rules,
            key=lambda r: (
                -r.pricing_rule.priority,
                -r.assigned_at.timestamp()
            )
        )

        for rule in stackable_rules:
            final_price = rule.pricing_rule.apply(
                current_price=final_price
            )
            applied.append(rule)

        return PricingCalculationResult(
            final_price=final_price.quantize(Decimal("0.01")),
            applied_rules=applied,
            latest_applied_rule=applied[-1] if applied else None
        )
    
def get_pricing_calculator() -> ProductPricingCalculator:
    return ProductPricingCalculator()