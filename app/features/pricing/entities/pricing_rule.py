from datetime import datetime
from decimal import Decimal
from app.features.pricing.types import PricingRuleType
from app.features.pricing.strategy.registry import (
    PRICING_STRATEGIES
)

class PricingRule:
    def __init__(
        self,
        id: int | None = None,
        name: str = "",
        description: str | None = None,
        type: PricingRuleType = PricingRuleType.PERCENTAGE,
        value: Decimal = Decimal("0"),
        is_active: bool = True,
        is_stackable: bool = True,
        priority: int = 0,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.value = value
        self.is_active = is_active
        self.is_stackable = is_stackable
        self.priority = priority
        self.starts_at = starts_at
        self.ends_at = ends_at
        self.created_at = created_at
        self.updated_at = updated_at

        self.validate()

    @property
    def strategy(self):
        return PRICING_STRATEGIES[self.type]

    def validate(self):
        self.strategy.validate(self.value)

    def apply(
        self,
        current_price: Decimal
    ) -> Decimal:

        return self.strategy.apply(
            current_price=current_price,
            rule=self.value
        )
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "value": str(self.value),
            "is_active": self.is_active,
            "is_stackable": self.is_stackable,
            "priority": self.priority,
            "starts_at": (
                self.starts_at.isoformat()
                if self.starts_at else None
            ),
            "ends_at": (
                self.ends_at.isoformat()
                if self.ends_at else None
            ),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at else None
            ),
        }