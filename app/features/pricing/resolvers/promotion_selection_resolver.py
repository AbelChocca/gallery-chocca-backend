from app.features.pricing.dtos.promotion_dto import (
    PromotionProductCandidateDTO,
)
from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.types.promotion_types import (
    PromotionStackingMode,
)


class PromotionSelectionResolver:

    def resolve(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
    ) -> dict[int, list[Promotion]]:
        promotions_by_product: dict[int, list[Promotion]] = {}

        for candidate in candidates:
            promotions = promotions_by_product.setdefault(
                candidate.product_id,
                [],
            )

            self._resolve_promotion_conflict(
                promotions=promotions,
                candidate=candidate.promotion,
            )

        return promotions_by_product

    def _resolve_promotion_conflict(
        self,
        *,
        promotions: list[Promotion],
        candidate: Promotion,
    ) -> None:

        if candidate.stacking_mode == PromotionStackingMode.STACKABLE:
            if any(
                promotion.stacking_mode
                == PromotionStackingMode.EXCLUSIVE
                for promotion in promotions
            ):
                return

            promotions.append(candidate)
            return

        if not promotions:
            promotions.append(candidate)
            return

        winner = candidate

        for promotion in promotions:
            winner = self._resolve_winner(
                current=promotion,
                candidate=winner,
            )

        if winner is candidate:
            promotions.clear()
            promotions.append(candidate)

    def _resolve_winner(
        self,
        *,
        current: Promotion,
        candidate: Promotion,
    ) -> Promotion:

        if candidate.priority > current.priority:
            return candidate

        if candidate.priority < current.priority:
            return current

        if candidate.created_at > current.created_at:
            return candidate

        return current