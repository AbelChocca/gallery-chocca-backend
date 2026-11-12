from dataclasses import dataclass
from datetime import datetime

from app.core.exceptions import ValidationError

@dataclass(slots=True)
class Coupon:
    id: int | None
    promotion_id: int
    code: str
    is_active: bool
    starts_at: datetime | None
    ends_at: datetime | None
    max_redemptions: int | None
    max_redemptions_per_customer: int | None
    used_count: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def validate(self) -> None:
        if not self.code.strip():
            raise ValidationError(
                "El código del cupón no puede estar vacío.",
                {
                    "entity": "Coupon",
                    "event": "validate",
                    "promotion_id": self.promotion_id,
                },
            )

        if (
            self.max_redemptions is not None
            and self.max_redemptions < 0
        ):
            raise ValidationError(
                "El máximo de canjes no puede ser negativo.",
                {
                    "entity": "Coupon",
                    "event": "validate",
                    "coupon_id": self.id,
                    "max_redemptions": self.max_redemptions,
                },
            )

        if (
            self.max_redemptions_per_customer is not None
            and self.max_redemptions_per_customer < 0
        ):
            raise ValidationError(
                "El máximo de canjes por cliente no puede ser negativo.",
                {
                    "entity": "Coupon",
                    "event": "validate",
                    "coupon_id": self.id,
                    "max_redemptions_per_customer":
                        self.max_redemptions_per_customer,
                },
            )

        if (
            self.starts_at is not None
            and self.ends_at is not None
            and self.ends_at <= self.starts_at
        ):
            raise ValidationError(
                "La fecha de fin debe ser posterior a la fecha de inicio.",
                {
                    "entity": "Coupon",
                    "event": "validate",
                    "coupon_id": self.id,
                    "starts_at": str(self.starts_at),
                    "ends_at": str(self.ends_at),
                },
            )