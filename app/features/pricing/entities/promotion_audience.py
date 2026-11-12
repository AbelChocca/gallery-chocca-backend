from dataclasses import dataclass
from datetime import datetime

from app.features.pricing.types.promotion_types import PromotionAudienceType
from app.core.exceptions import ValidationError

@dataclass(slots=True)
class PromotionAudience:
    promotion_id: int
    audience_type: PromotionAudienceType
    reference_id: int | None
    reference_value: str | None
    id: int | None = None
    created_at: datetime | None = None

    def validate(self) -> None:

        if self.audience_type == PromotionAudienceType.ALL_CUSTOMERS:
            if (
                self.reference_id is not None
                or self.reference_value is not None
            ):
                raise ValidationError(
                    "'TODOS LOS CLIENTES' no puede tener referencias."
                )

            return

        if self.audience_type == PromotionAudienceType.CUSTOMER:
            if (
                self.reference_id is None
                or self.reference_value is not None
            ):
                raise ValidationError(
                    "'CLIENTE' solo requiere una referencia por id.."
                )

            return

        if self.audience_type == PromotionAudienceType.CUSTOMER_GROUP:
            if (
                self.reference_value is None
                or self.reference_id is not None
            ):
                raise ValidationError(
                    "'GRUPO DE CLIENTES' solo requiere un valor de referencia."
                )