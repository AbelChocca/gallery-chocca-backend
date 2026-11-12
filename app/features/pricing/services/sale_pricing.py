from decimal import Decimal
from dataclasses import replace

from app.features.pricing.calculators.pricing_item_calculator import (
    PricingItemCalculator,
)
from app.features.pricing.calculators.pricing_subtotal_calculator import (
    PricingSubtotalCalculator,
)
from app.features.pricing.dtos.cart_pricing_dto import (
    AppliedPromotionDTO,
)
from app.features.pricing.dtos.promotion_dto import (
    PromotionCandidateCriteria,
    PromotionProductCandidateDTO,
)
from app.features.pricing.dtos.promotion_audience_dto import (
    PromotionAudienceContext,
)
from app.features.pricing.dtos.sale_pricing import (
    PricingItemResultDTO,
    SalePricingContext,
    SalePricingDTO,
)
from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.repositories.coupon_redemption_repository import (
    CouponRedemptionRepository,
)
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
from app.features.pricing.resolvers.promotion_resolver import (
    PromotionResolver,
)
from app.features.pricing.resolvers.promotion_selection_resolver import (
    PromotionSelectionResolver,
)
from app.features.pricing.types.promotion_types import (
    PromotionApplicationScope,
    PromotionTargetType,
)
from app.core.exceptions import ValueNotFound

class SalePricingService:

    def __init__(
        self,
        *,
        promotion_repository: PromotionRepository,
        coupon_repository: CouponRepository,
        coupon_redemption_repository: CouponRedemptionRepository,
        coupon_resolver: CouponResolver,
        promotion_resolver: PromotionResolver,
        promotion_audience_resolver: PromotionAudienceResolver,
        promotion_selection_resolver: PromotionSelectionResolver,
        promotion_condition_resolver: PromotionConditionResolver,
        pricing_item_calculator: PricingItemCalculator,
        pricing_subtotal_calculator: PricingSubtotalCalculator,
    ) -> None:
        self._promotion_repository = promotion_repository
        self._coupon_repository = coupon_repository
        self._coupon_redemption_repository = (
            coupon_redemption_repository
        )
        self._coupon_resolver = coupon_resolver
        self._promotion_resolver = promotion_resolver
        self._promotion_audience_resolver = (
            promotion_audience_resolver
        )
        self._promotion_selection_resolver = (
            promotion_selection_resolver
        )
        self._promotion_condition_resolver = (
            promotion_condition_resolver
        )
        self._pricing_item_calculator = (
            pricing_item_calculator
        )
        self._pricing_subtotal_calculator = (
            pricing_subtotal_calculator
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

        coupon_promotion_ids: set[int] = set()

        if context.coupon_code:
            coupon_candidates = await self._resolve_coupon_candidates(
                context=context,
                criteria=criteria,
            )

            coupon_promotion_ids = {
                candidate.promotion.id
                for candidate in coupon_candidates
            }

            existing = {
                (
                    candidate.product_id,
                    candidate.promotion.id,
                )
                for candidate in candidates
            }

            candidates.extend(
                candidate
                for candidate in coupon_candidates
                if (
                    candidate.product_id,
                    candidate.promotion.id,
                )
                not in existing
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

        result = self._calculate_sale_prices(
            context=context,
            promotions_by_product=promotions_by_product,
        )

        if context.coupon_code:
            result.applied_promotions = [
                replace(
                    promotion,
                    coupon_code=context.coupon_code,
                )
                if promotion.promotion_id in coupon_promotion_ids
                else promotion
                for promotion in result.applied_promotions
            ]

        return result

    def _calculate_sale_prices(
        self,
        *,
        context: SalePricingContext,
        promotions_by_product: dict[
            int,
            list[Promotion],
        ],
    ) -> SalePricingDTO:
        results: list[PricingItemResultDTO] = []

        subtotal = Decimal("0.00")
        item_discount_amount = Decimal("0.00")

        shipping_cost = context.shipping_cost

        promotion_totals: dict[
            int,
            AppliedPromotionDTO,
        ] = {}

        order_subtotal_promotions: dict[
            int,
            Promotion,
        ] = {}

        for item in context.items:
            promotions = promotions_by_product.get(
                item.product_id,
                [],
            )

            per_item_promotions = [
                promotion
                for promotion in promotions
                if (
                    promotion.application_scope
                    == PromotionApplicationScope.PER_ITEM
                )
            ]

            for promotion in promotions:
                if (
                    promotion.application_scope
                    == PromotionApplicationScope.ORDER_SUBTOTAL
                ):
                    order_subtotal_promotions[
                        promotion.id
                    ] = promotion

            calculation = (
                self._pricing_item_calculator.calculate(
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                    promotions=per_item_promotions,
                    shipping_cost=shipping_cost,
                )
            )

            shipping_cost = calculation.shipping_cost

            subtotal += calculation.original_total
            item_discount_amount += (
                calculation.discount_amount
            )

            results.append(
                PricingItemResultDTO(
                    item_id=item.item_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    original_unit_price=(
                        calculation.original_unit_price
                    ),
                    final_unit_price=(
                        calculation.final_unit_price
                    ),
                    original_total=(
                        calculation.original_total
                    ),
                    final_total=(
                        calculation.final_total
                    ),
                    discount_amount=(
                        calculation.discount_amount
                    ),
                    applied_promotions=(
                        calculation.applied_promotions
                    ),
                )
            )

            self._merge_applied_promotions(
                promotion_totals=promotion_totals,
                applied_promotions=(
                    calculation.applied_promotions
                ),
            )

        current_subtotal = sum(
            (
                item.final_total
                for item in results
            ),
            Decimal("0.00"),
        )

        resolved_order_promotions = (
            self._promotion_selection_resolver.resolve_promotions(
                promotions=list(
                    order_subtotal_promotions.values()
                ),
            )
        )

        subtotal_calculation = (
            self._pricing_subtotal_calculator.calculate(
                subtotal=current_subtotal,
                promotions=resolved_order_promotions,
            )
        )

        self._merge_applied_promotions(
            promotion_totals=promotion_totals,
            applied_promotions=(
                subtotal_calculation.applied_promotions
            ),
        )

        discount_amount = (
            item_discount_amount
            + subtotal_calculation.discount_amount
        )

        total = (
            subtotal_calculation.final_subtotal
            + shipping_cost
        )

        return SalePricingDTO(
            items=results,
            subtotal=subtotal,
            discount_amount=discount_amount,
            shipping_cost=shipping_cost,
            total=total,
            applied_promotions=list(
                promotion_totals.values()
            ),
        )

    @staticmethod
    def _merge_applied_promotions(
        *,
        promotion_totals: dict[
            int,
            AppliedPromotionDTO,
        ],
        applied_promotions: list[
            AppliedPromotionDTO
        ],
    ) -> None:
        for promotion in applied_promotions:
            existing = promotion_totals.get(
                promotion.promotion_id
            )

            if existing is None:
                promotion_totals[
                    promotion.promotion_id
                ] = promotion
                continue

            promotion_totals[promotion.promotion_id] = AppliedPromotionDTO(
                promotion_id=promotion.promotion_id,
                name=promotion.name,
                discount_amount=(
                    existing.discount_amount
                    + promotion.discount_amount
                ),
                application_scope=existing.application_scope,
                coupon_code=existing.coupon_code or promotion.coupon_code,
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
            raise ValueNotFound(
                "La promocion asociado al cupon no fue encontrado."
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
                    for product_id, category
                    in criteria.categories.items()
                    if category.value == target.reference_value
                )
                continue

            if target.target_type == PromotionTargetType.BRAND:
                product_ids.extend(
                    product_id
                    for product_id, brand
                    in criteria.brands.items()
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