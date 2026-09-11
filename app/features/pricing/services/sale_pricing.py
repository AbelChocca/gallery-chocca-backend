from app.features.pricing.calculators.pricing_calculator import PricingCalculator

from app.features.pricing.dtos.promotion_dto import (
    PromotionCandidateCriteria,
    PromotionProductCandidateDTO,
)

from app.features.pricing.dtos.sale_pricing import (
    SalePricingContext,
    SalePricingDTO,
)

from app.features.pricing.entities.promotion import Promotion

from app.features.pricing.repositories.coupon_repsitory import (
    CouponRepository,
)

from app.features.pricing.repositories.promotion_repository import (
    PromotionRepository,
)

from app.features.pricing.resolvers.coupon_resolver import (
    CouponResolver,
)

from app.features.pricing.resolvers.promotion_audience_resolver import (
    PromotionAudienceResolver,
)

from app.features.pricing.resolvers.promotion_condition_resolver import (
    PromotionConditionResolver,
)

from app.features.pricing.types.promotion_types import (
    PromotionStackingMode,
    PromotionTargetType,
)


class SalePricingService:

    def __init__(
        self,
        *,
        promotion_repository: PromotionRepository,
        coupon_repository: CouponRepository,
        pricing_calculator: PricingCalculator,
        coupon_resolver: CouponResolver,
        promotion_audience_resolver: PromotionAudienceResolver,
        promotion_condition_resolver: PromotionConditionResolver,
    ) -> None:
        self._promotion_repository = promotion_repository
        self._coupon_repository = coupon_repository
        self._pricing_calculator = pricing_calculator
        self._coupon_resolver = coupon_resolver
        self._promotion_audience_resolver = (
            promotion_audience_resolver
        )
        self._promotion_condition_resolver = (
            promotion_condition_resolver
        )

    async def calculate(
        self,
        *,
        context: SalePricingContext,
    ) -> SalePricingDTO:

        criteria = PromotionCandidateCriteria(
            product_ids=[
                item.product_id
                for item in context.items
            ],
            categories={
                item.product_id: item.category
                for item in context.items
            },
            brands={
                item.product_id: item.brand
                for item in context.items
            },
            sale_channel=context.sale_channel,
        )

        candidates = await (
            self._promotion_repository.find_candidates(
                criteria=criteria,
            )
        )

        if context.coupon_code:
            coupon_candidates = await self._resolve_coupon_candidates(
                context=context,
                criteria=criteria,
            )

            candidates.extend(coupon_candidates)

        candidates = self._filter_by_audience(
            candidates=candidates,
            context=context,
        )

        candidates = self._filter_by_conditions(
            candidates=candidates,
            context=context,
        )

        promotions_by_product = self._map_promotions(
            candidates=candidates,
        )

        return self._pricing_calculator.calculate(
            context=context,
            promotions_by_product=promotions_by_product,
        )

    async def _resolve_coupon_candidates(
        self,
        *,
        context: SalePricingContext,
        criteria: PromotionCandidateCriteria,
    ) -> list[PromotionProductCandidateDTO]:

        coupon = await self._coupon_repository.get_by_code(
            code=context.coupon_code,
        )

        if coupon is None:
            raise ValueError("Coupon not found.")

        self._coupon_resolver.validate(
            coupon=coupon,
            now=context.now,
        )

        promotion = await (
            self._promotion_repository.get_by_id_with_details(
                promotion_id=coupon.promotion_id,
            )
        )

        if promotion is None:
            raise ValueError(
                "The promotion associated with the coupon was not found."
            )

        product_ids = self._resolve_promotion_product_ids(
            promotion=promotion,
            criteria=criteria,
        )

        return [
            PromotionProductCandidateDTO(
                product_id=product_id,
                promotion=promotion,
            )
            for product_id in product_ids
        ]

    def _resolve_promotion_product_ids(
        self,
        *,
        promotion: Promotion,
        criteria: PromotionCandidateCriteria,
    ) -> list[int]:

        product_ids: list[int] = []

        for target in promotion.targets:

            if target.target_type == PromotionTargetType.ALL:
                product_ids.extend(criteria.product_ids)
                continue

            if target.target_type == PromotionTargetType.PRODUCT:
                if target.reference_id in criteria.product_ids:
                    product_ids.append(target.reference_id)

                continue

            if target.target_type == PromotionTargetType.CATEGORY:
                product_ids.extend(
                    product_id
                    for product_id, category in criteria.categories.items()
                    if category.value == target.reference_value
                )
                continue

            if target.target_type == PromotionTargetType.BRAND:
                product_ids.extend(
                    product_id
                    for product_id, brand in criteria.brands.items()
                    if brand.value == target.reference_value
                )

        return list(dict.fromkeys(product_ids))

    def _map_promotions(
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

    def _filter_by_audience(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
        context: SalePricingContext,
    ) -> list[PromotionProductCandidateDTO]:

        return [
            candidate
            for candidate in candidates
            if self._promotion_audience_resolver.matches_promotion(
                audiences=candidate.promotion.audiences,
                context=context,
            )
        ]

    def _filter_by_conditions(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
        context: SalePricingContext,
    ) -> list[PromotionProductCandidateDTO]:

        return [
            candidate
            for candidate in candidates
            if self._promotion_condition_resolver.matches_all(
                conditions=candidate.promotion.conditions,
                context=context,
            )
        ]