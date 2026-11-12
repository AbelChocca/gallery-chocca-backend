from dataclasses import dataclass
from datetime import datetime

from app.core.exceptions import ValidationError

from app.features.pricing.types.promotion_types import (
    PromotionTargetType,
)


@dataclass(slots=True)
class PromotionTarget:
    id: int | None
    promotion_id: int
    target_type: PromotionTargetType
    reference_id: int | None = None
    reference_value: str | None = None
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if self.target_type == PromotionTargetType.ALL:
            if (
                self.reference_id is not None
                or self.reference_value is not None
            ):
                raise ValidationError(
                    "El target global no debe tener referencias asociadas.",
                    {
                        "entity": "PromotionTarget",
                        "event": "validate",
                        "promotion_id": self.promotion_id,
                        "target_type": self.target_type.value,
                        "reference_id": self.reference_id,
                        "reference_value": self.reference_value,
                    },
                )

            return

        if self.target_type == PromotionTargetType.PRODUCT:
            if (
                self.reference_id is None
                or self.reference_value is not None
            ):
                raise ValidationError(
                    "El target de producto requiere únicamente 'reference_id'.",
                    {
                        "entity": "PromotionTarget",
                        "event": "validate",
                        "promotion_id": self.promotion_id,
                        "target_type": self.target_type.value,
                        "reference_id": self.reference_id,
                        "reference_value": self.reference_value,
                    },
                )

            return

        if self.target_type in {
            PromotionTargetType.CATEGORY,
            PromotionTargetType.BRAND,
            PromotionTargetType.COLLECTION,
        }:
            if (
                self.reference_id is not None
                or not self.reference_value
            ):
                raise ValidationError(
                    "El target requiere únicamente 'reference_value'.",
                    {
                        "entity": "PromotionTarget",
                        "event": "validate",
                        "promotion_id": self.promotion_id,
                        "target_type": self.target_type.value,
                        "reference_id": self.reference_id,
                        "reference_value": self.reference_value,
                    },
                )

            return

        raise ValidationError(
            "El tipo de target de promoción no es compatible.",
            {
                "entity": "PromotionTarget",
                "event": "validate",
                "promotion_id": self.promotion_id,
                "target_type": self.target_type.value,
            },
        )