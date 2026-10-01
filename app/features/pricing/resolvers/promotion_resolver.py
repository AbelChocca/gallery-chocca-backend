from datetime import datetime

from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.dtos.promotion_dto import (
    PromotionProductCandidateDTO,
)

class PromotionResolver:

    def is_available(
        self,
        *,
        promotion: Promotion,
        now: datetime,
    ) -> bool:
        if not promotion.is_active:
            return False

        if (
            promotion.starts_at is not None
            and now < promotion.starts_at
        ):
            return False

        if (
            promotion.ends_at is not None
            and now >= promotion.ends_at
        ):
            return False

        return True

    def filter_available(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
        now: datetime,
    ) -> list[PromotionProductCandidateDTO]:
        availability_cache: dict[int, bool] = {}

        result: list[PromotionProductCandidateDTO] = []

        for candidate in candidates:
            promotion = candidate.promotion

            if promotion.id not in availability_cache:
                availability_cache[promotion.id] = self.is_available(
                    promotion=promotion,
                    now=now,
                )

            if availability_cache[promotion.id]:
                result.append(candidate)

        return result


def get_promotion_resolver() -> PromotionResolver:
    return PromotionResolver()