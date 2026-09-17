from dataclasses import dataclass

from app.features.sales.types.customer import CustomerType


@dataclass(frozen=True)
class PromotionAudienceContext:
    customer_id: int | None = None
    customer_type: CustomerType | None = None