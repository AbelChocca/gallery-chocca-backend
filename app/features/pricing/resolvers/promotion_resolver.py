from datetime import datetime

from app.features.pricing.entities.promotion import Promotion
from app.core.exceptions import ValidationError


class PromotionResolver:

    def validate(
        self,
        *,
        promotion: Promotion,
        now: datetime,
    ) -> None:
        self._validate_active(
            promotion=promotion,
        )
        self._validate_start_date(
            promotion=promotion,
            now=now,
        )
        self._validate_end_date(
            promotion=promotion,
            now=now,
        )

    def _validate_active(
        self,
        *,
        promotion: Promotion,
    ) -> None:
        if not promotion.is_active:
            raise ValidationError(
                "La promocion esta inactiva."
            )

    def _validate_start_date(
        self,
        *,
        promotion: Promotion,
        now: datetime,
    ) -> None:
        if (
            promotion.starts_at is not None
            and now < promotion.starts_at
        ):
            raise ValidationError(
                "La promocion ya no se encuetra activo."
            )

    def _validate_end_date(
        self,
        *,
        promotion: Promotion,
        now: datetime,
    ) -> None:
        if (
            promotion.ends_at is not None
            and now >= promotion.ends_at
        ):
            raise ValidationError(
                "La promocion ha expirado"
            )