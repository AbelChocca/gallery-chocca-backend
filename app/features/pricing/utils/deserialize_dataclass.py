from app.features.pricing.types.pricing_rules_types import PricingRuleType
from app.features.pricing.types.promotion_types import (
    PromotionConditionType,
)

from app.features.sales.types.payment import (
    PaymentMethod,
)
from app.features.pricing.dtos.pricing_rule_dto import (
    PricingRuleParameters, 
    PercentageRuleParameters,
    FixedPriceRuleParameters,
    FixedAmountRuleParameters,
    FreeShippingRuleParameters,
    FreeItemRuleParameters,
    BuyXGetYRuleParameters
)
from app.features.pricing.dtos.promotion_condition import (
    PromotionConditionParameters,
    MinimumOrderAmountConditionParameters,
    MinimumProductQuantityConditionParameters,
    PaymentMethodConditionParameters
)
from decimal import Decimal


def deserialize_pricing_rules_parameters(
    rule_type: PricingRuleType,
    parameters: dict,
) -> PricingRuleParameters:

    if rule_type == PricingRuleType.PERCENTAGE:
        return PercentageRuleParameters(
            percentage=Decimal(
                parameters["percentage"]
            )
        )

    if rule_type == PricingRuleType.FIXED_AMOUNT:
        return FixedAmountRuleParameters(
            amount=Decimal(
                parameters["amount"]
            )
        )

    if rule_type == PricingRuleType.FIXED_PRICE:
        return FixedPriceRuleParameters(
            price=Decimal(
                parameters["price"]
            )
        )

    if rule_type == PricingRuleType.BUY_X_GET_Y:
        return BuyXGetYRuleParameters(
            buy_quantity=int(
                parameters["buy_quantity"]
            ),
            free_quantity=int(
                parameters["free_quantity"]
            ),
        )

    if rule_type == PricingRuleType.FREE_ITEM:
        return FreeItemRuleParameters(
            variant_size_id=int(
                parameters["variant_size_id"]
            ),
            quantity=int(
                parameters.get(
                    "quantity",
                    1,
                )
            ),
        )

    if rule_type == PricingRuleType.FREE_SHIPPING:
        return FreeShippingRuleParameters(
            applies=bool(
                parameters.get(
                    "applies",
                    True,
                )
            ),
        )

    raise ValueError(
        f"Unsupported pricing rule type: {rule_type}"
    )

def deserialize_promotion_condition_parameters(
    condition_type: PromotionConditionType,
    parameters: dict,
) -> PromotionConditionParameters:

    if (
        condition_type
        == PromotionConditionType.MINIMUM_ORDER_AMOUNT
    ):
        return MinimumOrderAmountConditionParameters(
            minimum_amount=Decimal(
                parameters["minimum_amount"]
            )
        )

    if (
        condition_type
        == PromotionConditionType.MINIMUM_PRODUCT_QUANTITY
    ):
        return MinimumProductQuantityConditionParameters(
            minimum_quantity=int(
                parameters["minimum_quantity"]
            )
        )

    if (
        condition_type
        == PromotionConditionType.PAYMENT_METHOD
    ):
        return PaymentMethodConditionParameters(
            payment_method=PaymentMethod(
                parameters["payment_method"]
            )
        )

    raise ValueError(
        f"Unsupported promotion condition type: {condition_type}"
    )