from app.features.pricing.calculators.pricing_calculator import PricingCalculator
from datetime import datetime

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
    PromotionTargetType,
)
from app.features.pricing.repositories.coupon_redemption_repository import (
    CouponRedemptionRepository,
)
from app.features.pricing.resolvers.promotion_resolver import PromotionResolver
from app.features.pricing.dtos.promotion_audience_dto import PromotionAudienceContext
from app.features.pricing.resolvers.promotion_selection_resolver import (
    PromotionSelectionResolver,
)


class SalePricingService:

    def __init__(
        self,
        *,
        promotion_repository: PromotionRepository,
        coupon_repository: CouponRepository,
        coupon_redemption_repository: CouponRedemptionRepository,
        pricing_calculator: PricingCalculator,
        coupon_resolver: CouponResolver,
        promotion_resolver: PromotionResolver,
        promotion_audience_resolver: PromotionAudienceResolver,
        promotion_selection_resolver: PromotionSelectionResolver,
        promotion_condition_resolver: PromotionConditionResolver,
    ) -> None:
        self._promotion_repository = promotion_repository
        self._coupon_repository = coupon_repository
        self._coupon_redemption_repository = coupon_redemption_repository
        self._pricing_calculator = pricing_calculator
        self._promotion_resolver = promotion_resolver
        self._promotion_selection_resolver = promotion_selection_resolver
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

        candidates = self._promotion_resolver.filter_available(
            candidates=candidates,
            now=context.now,
        )

        if context.coupon_code:
            coupon_candidates = await self._resolve_coupon_candidates(
                context=context,
                criteria=criteria,
            )

            existing = {
                (candidate.product_id, candidate.promotion.id)
                for candidate in candidates
            }

            candidates.extend(
                candidate
                for candidate in coupon_candidates
                if (candidate.product_id, candidate.promotion.id) not in existing
            )

        candidates = self._filter_by_audience(
            candidates=candidates,
            context=context,
        )

        candidates = self._filter_by_conditions(
            candidates=candidates,
            context=context,
        )

        promotions_by_product = (
            self._promotion_selection_resolver.resolve(
                candidates=candidates,
            )
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

        customer_redemptions = 0

        if context.customer_id is not None:
            customer_redemptions = (
                await self._coupon_redemption_repository
                .count_by_coupon_and_customer(
                    coupon_id=coupon.id,
                    customer_id=context.customer_id,
                )
            )

        self._coupon_resolver.validate(
            coupon=coupon,
            customer_redemptions=customer_redemptions,
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


    def _filter_by_audience(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
        context: SalePricingContext,
    ) -> list[PromotionProductCandidateDTO]:

        audience_context = PromotionAudienceContext(
            customer_id=context.customer_id,
            customer_type=context.customer_type,
        )

        return [
            candidate
            for candidate in candidates
            if self._promotion_audience_resolver.matches_promotion(
                audiences=candidate.promotion.audiences,
                context=audience_context,
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