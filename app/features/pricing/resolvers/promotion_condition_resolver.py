from decimal import Decimal
from typing import Any

from app.features.pricing.entities.promotion_condition import (
    PromotionCondition,
)
from app.features.pricing.dtos.sale_pricing import SalePricingContext
from app.features.pricing.types.promotion_types import PromotionConditionType


class PromotionConditionResolver:

    def matches(
        self,
        *,
        condition: PromotionCondition,
        context: SalePricingContext,
    ) -> bool:
        if (
            condition.condition_type
            == PromotionConditionType.MINIMUM_ORDER_AMOUNT
        ):
            return self._matches_minimum_order_amount(
                condition=condition,
                context=context,
            )

        if (
            condition.condition_type
            == PromotionConditionType.MINIMUM_PRODUCT_QUANTITY
        ):
            return self._matches_minimum_product_quantity(
                condition=condition,
                context=context,
            )

        if (
            condition.condition_type
            == PromotionConditionType.PAYMENT_METHOD
        ):
            return self._matches_payment_method(
                condition=condition,
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
                condition=condition,
                context=context,
            )
            for condition in conditions
        )

    def _matches_minimum_order_amount(
        self,
        *,
        condition: PromotionCondition,
        context: SalePricingContext,
    ) -> bool:
        minimum_amount = Decimal(
            str(condition.parameters["minimum_amount"])
        )

        order_amount = sum(
            item.unit_price * item.quantity
            for item in context.items
        )

        return order_amount >= minimum_amount

    def _matches_minimum_product_quantity(
        self,
        *,
        condition: PromotionCondition,
        context: SalePricingContext,
    ) -> bool:
        minimum_quantity = int(
            condition.parameters["minimum_quantity"]
        )

        total_quantity = sum(
            item.quantity
            for item in context.items
        )

        return total_quantity >= minimum_quantity

    def _matches_payment_method(
        self,
        *,
        condition: PromotionCondition,
        context: SalePricingContext,
    ) -> bool:
        expected_payment_method = condition.parameters["payment_method"]

        if context.payment_method is None:
            return False

        return context.payment_method.value == expected_payment_method