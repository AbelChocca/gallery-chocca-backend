from dataclasses import dataclass
from datetime import datetime

from app.core.exceptions import ValidationError

from app.features.pricing.types.promotion_types import (
    PromotionConditionType,
)

from app.features.pricing.dtos.promotion_condition import (
    PromotionConditionParameters,
    MinimumOrderAmountConditionParameters,
    MinimumProductQuantityConditionParameters,
    PaymentMethodConditionParameters,
)


@dataclass(slots=True)
class PromotionCondition:
    id: int | None
    promotion_id: int
    condition_type: PromotionConditionType
    parameters: PromotionConditionParameters
    description: str | None
    created_at: datetime | None = None

    def validate(self) -> None:
        if (
            self.condition_type
            == PromotionConditionType.MINIMUM_ORDER_AMOUNT
        ):
            self._validate_minimum_order_amount()
            return

        if (
            self.condition_type
            == PromotionConditionType.MINIMUM_PRODUCT_QUANTITY
        ):
            self._validate_minimum_product_quantity()
            return

        if (
            self.condition_type
            == PromotionConditionType.PAYMENT_METHOD
        ):
            self._validate_payment_method()
            return

        raise ValidationError(
            "El tipo de condición de promoción no es compatible.",
            {
                "entity": "PromotionCondition",
                "event": "validate",
                "promotion_id": self.promotion_id,
                "condition_type": self.condition_type.value,
            },
        )

    def _validate_minimum_order_amount(self) -> None:
        if not isinstance(
            self.parameters,
            MinimumOrderAmountConditionParameters,
        ):
            raise ValidationError(
                "Los parámetros no corresponden a una condición de monto mínimo.",
                {
                    "entity": "PromotionCondition",
                    "event": "validate_minimum_order_amount",
                    "promotion_id": self.promotion_id,
                    "condition_type": self.condition_type.value,
                    "parameters_type": type(self.parameters).__name__,
                },
            )

        if self.parameters.minimum_amount <= 0:
            raise ValidationError(
                "El monto mínimo debe ser mayor que cero.",
                {
                    "entity": "PromotionCondition",
                    "event": "validate_minimum_order_amount",
                    "promotion_id": self.promotion_id,
                    "condition_type": self.condition_type.value,
                    "minimum_amount": str(
                        self.parameters.minimum_amount
                    ),
                },
            )

    def _validate_minimum_product_quantity(self) -> None:
        if not isinstance(
            self.parameters,
            MinimumProductQuantityConditionParameters,
        ):
            raise ValidationError(
                "Los parámetros no corresponden a una condición de cantidad mínima de productos.",
                {
                    "entity": "PromotionCondition",
                    "event": "validate_minimum_product_quantity",
                    "promotion_id": self.promotion_id,
                    "condition_type": self.condition_type.value,
                    "parameters_type": type(self.parameters).__name__,
                },
            )

        if self.parameters.minimum_quantity <= 0:
            raise ValidationError(
                "La cantidad mínima de productos debe ser mayor que cero.",
                {
                    "entity": "PromotionCondition",
                    "event": "validate_minimum_product_quantity",
                    "promotion_id": self.promotion_id,
                    "condition_type": self.condition_type.value,
                    "minimum_quantity": self.parameters.minimum_quantity,
                },
            )

    def _validate_payment_method(self) -> None:
        if not isinstance(
            self.parameters,
            PaymentMethodConditionParameters,
        ):
            raise ValidationError(
                "Los parámetros no corresponden a una condición de método de pago.",
                {
                    "entity": "PromotionCondition",
                    "event": "validate_payment_method",
                    "promotion_id": self.promotion_id,
                    "condition_type": self.condition_type.value,
                    "parameters_type": type(self.parameters).__name__,
                },
            )