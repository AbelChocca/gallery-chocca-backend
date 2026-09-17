from datetime import datetime
from decimal import Decimal

from app.features.pricing.calculators.pricing_item_calculator import (
    PricingItemCalculator,
)

from app.features.pricing.dtos.cart_pricing_dto import (
    CartPricingContext,
    CartPricingDTO,
    CartPricingItemResultDTO,
)

from app.features.pricing.dtos.promotion_dto import (
    PromotionCandidateCriteria,
    PromotionProductCandidateDTO,
)

from app.features.pricing.dtos.promotion_audience_dto import (
    PromotionAudienceContext,
)

from app.features.pricing.dtos.sale_pricing import (
    PricingItemDTO,
    SalePricingContext,
)

from app.features.pricing.entities.promotion import Promotion

from app.features.pricing.repositories.promotion_repository import (
    PromotionRepository,
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
    PromotionConditionType,
)


class CartPricingService:

    def __init__(
        self,
        *,
        promotion_repository: PromotionRepository,
        promotion_resolver: PromotionResolver,
        promotion_selection_resolver: PromotionSelectionResolver,
        promotion_audience_resolver: PromotionAudienceResolver,
        promotion_condition_resolver: PromotionConditionResolver,
        pricing_item_calculator: PricingItemCalculator,
    ) -> None:
        self._promotion_repository = promotion_repository
        self._promotion_resolver = promotion_resolver
        self._promotion_selection_resolver = (
            promotion_selection_resolver
        )
        self._promotion_audience_resolver = (
            promotion_audience_resolver
        )
        self._promotion_condition_resolver = (
            promotion_condition_resolver
        )
        self._pricing_item_calculator = (
            pricing_item_calculator
        )

    async def calculate(
        self,
        *,
        context: CartPricingContext,
    ) -> CartPricingDTO:

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

        candidates = await self._promotion_repository.find_candidates(
            criteria=criteria,
        )

        self._validate_promotions(
            candidates=candidates,
            now=context.now,
        )

        candidates = self._filter_by_audience(
            candidates=candidates,
            context=context,
        )

        candidates = self._filter_cart_eligible_promotions(
            candidates=candidates,
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

        return self._calculate_cart_prices(
            context=context,
            promotions_by_product=promotions_by_product,
        )

    def _filter_by_audience(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
        context: CartPricingContext,
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

    def _filter_cart_eligible_promotions(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
    ) -> list[PromotionProductCandidateDTO]:

        allowed_conditions = {
            PromotionConditionType.MINIMUM_ORDER_AMOUNT,
            PromotionConditionType.MINIMUM_PRODUCT_QUANTITY,
        }

        return [
            candidate
            for candidate in candidates
            if all(
                condition.condition_type in allowed_conditions
                for condition in candidate.promotion.conditions
            )
        ]

    def _filter_by_conditions(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
        context: CartPricingContext,
    ) -> list[PromotionProductCandidateDTO]:

        condition_context = SalePricingContext(
            items=[
                PricingItemDTO(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    category=item.category,
                    brand=item.brand,
                    unit_price=item.unit_price,
                )
                for item in context.items
            ],
            sale_channel=context.sale_channel,
            customer_id=context.customer_id,
            customer_type=context.customer_type,
            coupon_code=None,
            payment_method=None,
            shipping_cost=Decimal("0.00"),
            now=context.now,
        )

        return [
            candidate
            for candidate in candidates
            if self._promotion_condition_resolver.matches_all(
                conditions=candidate.promotion.conditions,
                context=condition_context,
            )
        ]

    def _calculate_cart_prices(
        self,
        *,
        context: CartPricingContext,
        promotions_by_product: dict[int, list[Promotion]],
    ) -> CartPricingDTO:

        results: list[CartPricingItemResultDTO] = []

        subtotal = Decimal("0.00")
        discount_amount = Decimal("0.00")

        for item in context.items:

            promotions = promotions_by_product.get(
                item.product_id,
                [],
            )

            calculation = self._pricing_item_calculator.calculate(
                unit_price=item.unit_price,
                quantity=item.quantity,
                promotions=promotions,
            )

            subtotal += calculation.original_total
            discount_amount += calculation.discount_amount

            results.append(
                CartPricingItemResultDTO(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    original_unit_price=calculation.original_unit_price,
                    final_unit_price=calculation.final_unit_price,
                    original_total=calculation.original_total,
                    final_total=calculation.final_total,
                    discount_amount=calculation.discount_amount,
                )
            )

        return CartPricingDTO(
            items=results,
            subtotal=subtotal,
            discount_amount=discount_amount,
            total=subtotal - discount_amount,
        )

    def _validate_promotions(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
        now: datetime,
    ) -> None:

        validated: set[int] = set()

        for candidate in candidates:
            promotion = candidate.promotion

            if promotion.id in validated:
                continue

            self._promotion_resolver.validate(
                promotion=promotion,
                now=now,
            )

            validated.add(promotion.id)