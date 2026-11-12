from dataclasses import dataclass
from datetime import datetime
from app.core.exceptions import ValidationError

@dataclass
class PromotionPricingRule:
    promotion_id: int
    pricing_rule_id: int
    execution_order: int = 0
    assigned_at: datetime | None = None

    def validate(self) -> None:
        if self.execution_order < 0:
            raise ValidationError(
                "El orden de ejecucion no puede ser negativo"
            )