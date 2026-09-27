from app.features.pricing.entities.promotion_condition import (
    PromotionCondition,
    PromotionConditionParameters,
    MinimumProductQuantityConditionParameters,
    MinimumOrderAmountConditionParameters,
    PaymentMethodConditionParameters
)
from app.features.pricing.dtos.sale_pricing import SalePricingContext
from app.features.pricing.types.promotion_types import PromotionConditionType


class PromotionConditionResolver:

    """
    Expected condition parameters:

    MINIMUM_ORDER_AMOUNT:
        {"minimum_amount": "100.00"}

    MINIMUM_PRODUCT_QUANTITY:
        {"minimum_quantity": 2}

    PAYMENT_METHOD:
        {"payment_method": "YAPE"}
    """

    def matches(
        self,
        *,
        condition_type: PromotionConditionType,
        parameters: PromotionConditionParameters,
        context: SalePricingContext,
    ) -> bool:
        if (
            condition_type
            == PromotionConditionType.MINIMUM_ORDER_AMOUNT
        ):
            return self._matches_minimum_order_amount(
                parameters=parameters,
                context=context,
            )

        if (
            condition_type
            == PromotionConditionType.MINIMUM_PRODUCT_QUANTITY
        ):
            return self._matches_minimum_product_quantity(
                parameters=parameters,
                context=context,
            )

        if (
            condition_type
            == PromotionConditionType.PAYMENT_METHOD
        ):
            return self._matches_payment_method(
                parameters=parameters,
                context=context,
            )

        return False

    def matches_all(
        self,
        *,
        conditions: list[PromotionCondition],
        context: SalePricingContext,
    ) -> bool:
        return all(
            self.matches(
                condition_type=condition.condition_type,
                parameters=condition.parameters,
                context=context,
            )
            for condition in conditions
        )

    def _matches_minimum_order_amount(
        self,
        *,
        parameters: MinimumOrderAmountConditionParameters,
        context: SalePricingContext,
    ) -> bool:
        minimum_amount = parameters.minimum_amount

        order_amount = sum(
            item.unit_price * item.quantity
            for item in context.items
        )

        return order_amount >= minimum_amount

    def _matches_minimum_product_quantity(
        self,
        *,
        parameters: MinimumProductQuantityConditionParameters,
        context: SalePricingContext,
    ) -> bool:
        minimum_quantity = parameters.minimum_quantity

        total_quantity = sum(
            item.quantity
            for item in context.items
        )

        return total_quantity >= minimum_quantity

    def _matches_payment_method(
        self,
        *,
        parameters: PaymentMethodConditionParameters,
        context: SalePricingContext,
    ) -> bool:
        expected_payment_method = parameters.payment_method.value

        if context.payment_method is None:
            return False

        return context.payment_method.value == expected_payment_method

def get_condition_resolver() -> PromotionConditionResolver:
    return PromotionConditionResolver()