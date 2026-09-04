from abc import ABC, abstractmethod

from app.features.pricing.dtos.promotion_dto import AppliedPromotionDTO
from app.features.pricing.dtos.sale_pricing import SalePricingContext

class PromotionValidator(ABC):

    @abstractmethod
    def validate(
        self,
        *,
        promotion: AppliedPromotionDTO,
        context: SalePricingContext,
    ) -> bool:
        ...

#ValidityValidator

#AudienceValidator

#TargetValidator

#ConditionValidator