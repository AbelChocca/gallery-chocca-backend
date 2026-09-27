from datetime import datetime

from app.features.pricing.dtos.promotion_dto import (
    PromotionCandidateCriteria,
    PromotionProductCandidateDTO,
)

from app.features.pricing.dtos.catalog_pricing_dto import (
    CatalogPricingContext,
    CatalogPricingItemResultDTO,
)

from app.features.pricing.dtos.promotion_audience_dto import (
    PromotionAudienceContext,
)

from app.features.pricing.repositories.promotion_repository import (
    PromotionRepository,
)

from app.features.pricing.resolvers.promotion_audience_resolver import (
    PromotionAudienceResolver,
)

from app.features.pricing.resolvers.promotion_resolver import (
    PromotionResolver,
)
from app.features.pricing.resolvers.promotion_selection_resolver import PromotionSelectionResolver
from app.features.pricing.calculators.pricing_item_calculator import (
    PricingItemCalculator,
)
from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.types.promotion_types import (
    PromotionApplicationScope,
)


class CatalogPricingService:

    def __init__(
        self,
        *,
        promotion_repository: PromotionRepository,
        promotion_resolver: PromotionResolver,
        promotion_selection_resolver: PromotionSelectionResolver,
        promotion_audience_resolver: PromotionAudienceResolver,
        pricing_item_calculator: PricingItemCalculator,
    ) -> None:
        self._promotion_repository = promotion_repository
        self._promotion_resolver = promotion_resolver
        self._promotion_selection_resolver = promotion_selection_resolver
        self._promotion_audience_resolver = promotion_audience_resolver
        self._pricing_item_calculator = pricing_item_calculator

    async def calculate(
        self,
        *,
        context: CatalogPricingContext,
    ) -> list[CatalogPricingItemResultDTO]:

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

        candidates = self._filter_catalog_eligible_promotions(
            candidates=candidates,
        )

        promotions_by_product = self._promotion_selection_resolver.resolve(
            candidates=candidates,
        )

        return self._calculate_catalog_prices(
            context=context,
            promotions_by_product=promotions_by_product,
        )

    def _filter_by_audience(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
        context: CatalogPricingContext,
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

    def _filter_catalog_eligible_promotions(
        self,
        *,
        candidates: list[PromotionProductCandidateDTO],
    ) -> list[PromotionProductCandidateDTO]:

        return [
            candidate
            for candidate in candidates
            if (
                not candidate.promotion.conditions
                and candidate.promotion.application_scope
                == PromotionApplicationScope.PER_ITEM
            )
        ]

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

    def _calculate_catalog_prices(
        self,
        *,
        context: CatalogPricingContext,
        promotions_by_product: dict[int, list[Promotion]],
    ) -> list[CatalogPricingItemResultDTO]:

        results: list[CatalogPricingItemResultDTO] = []

        for item in context.items:
            promotions = promotions_by_product.get(
                item.product_id,
                [],
            )

            calculation = self._pricing_item_calculator.calculate(
                unit_price=item.unit_price,
                quantity=1,
                promotions=promotions,
            )

            results.append(
                CatalogPricingItemResultDTO(
                    product_id=item.product_id,
                    original_price=calculation.original_unit_price,
                    final_price=calculation.final_unit_price,
                    discount_amount=calculation.discount_amount,
                )
            )

        return results