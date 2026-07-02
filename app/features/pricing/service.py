from app.infra.db.repositories.sqlalchemy_pricing_rule_repository import (
    PricingRuleRepository
)

from app.infra.db.repositories.sqlalchemy_product_pricing_rule_repository import (
    ProductPricingRepository
)

from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.features.products.dto.product_dto import FilterProductCommand

from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.entities.product_applied_pricing_rule import ProductAppliedPricingRule
from app.features.pricing.utils.pricing_calculator import ProductPricingCalculator
from app.features.pricing.types import PricingRuleType, ProductPricingSummaryTD

from app.shared.pagination.pagination_service import PaginationService

from app.core.exceptions import ValueNotFound, InvalidOperation
from collections import defaultdict
from decimal import Decimal


class PricingService:
    def __init__(
        self,
        pricing_rule_repository: PricingRuleRepository,
        product_pricing_repository: ProductPricingRepository,
        product_repository: PostgresProductRepository,
        pricing_calculator: ProductPricingCalculator,
        pagination_service: PaginationService
    ):
        self._pricing_rule_repository = pricing_rule_repository
        self._product_pricing_repository = product_pricing_repository
        self._pricing_calculator = pricing_calculator
        self._product_repository = product_repository
        self._pagination_service = pagination_service

    # =========================================================
    # PRICING RULES
    # =========================================================

    async def create_pricing_rule(
        self,
        *,
        name: str,
        description: str | None,
        type: str,
        value: Decimal,
        priority: int = 0,
        is_active: bool = True,
        is_stackable: bool = True
    ) -> PricingRule:

        pricing_rule = PricingRule(
            name=name,
            description=description,
            type=type,
            value=value,
            priority=priority,
            is_active=is_active,
            is_stackable=is_stackable
        )

        created_rule = await (
            self._pricing_rule_repository.save(pricing_rule)
        )

        return created_rule

    async def get_pricing_rule(
        self,
        rule_id: int
    ) -> PricingRule:

        rule = await self._pricing_rule_repository.get_pricing_rule_by_id(
            rule_id
        )

        if not rule:
            raise ValueNotFound(
                "Pricing rule not found",
                {"rule_id": rule_id}
            )

        return rule

    async def get_pricing_rules(
        self,
        *,
        is_active: bool | None = None,
        type: PricingRuleType | None = None,
        priority_min: int | None = None,
        priority_max: int | None = None,
        search: str | None = None,
        limit: int = 50,
        page: int = 1
    ) -> dict:
        offset = self._pagination_service.get_offset(page, limit)

        total = await self._pricing_rule_repository.count_pricing_rules(
            is_active=is_active,
            type=type,
            priority_max=priority_max,
            priority_min=priority_min,
            search=search
        )

        current_page = self._pagination_service.get_current_page(offset, limit)
        total_pages = self._pagination_service.get_total_pages(total, limit)

        pricing_rules = await self._pricing_rule_repository.get_pricing_rules(
            is_active=is_active,
            type=type,
            priority_min=priority_min,
            priority_max=priority_max,
            search=search,
            limit=limit,
            offset=offset
        )

        return {
            "total": total,
            "items": pricing_rules,
            "pagination": {
                "current_page": current_page,
                "total_pages": total_pages
            }
        }

    async def activate_pricing_rule(
        self,
        rule_id: int
    ) -> None:

        pricing_rule = await (
            self._pricing_rule_repository
            .get_pricing_rule_by_id(rule_id)
        )

        if not pricing_rule:
            raise ValueNotFound(
                "Pricing rule not found",
                {"rule_id": rule_id}
            )

        if pricing_rule.is_active:
            raise InvalidOperation(
                "Pricing rule is already active"
            )

        await (
            self._pricing_rule_repository
            .activate_pricing_rule(rule_id)
        )


    async def deactivate_pricing_rule(
        self,
        rule_id: int
    ) -> None:

        pricing_rule = await (
            self._pricing_rule_repository
            .get_pricing_rule_by_id(rule_id)
        )

        if not pricing_rule:
            raise ValueNotFound(
                "Pricing rule not found",
                {"rule_id": rule_id}
            )

        if not pricing_rule.is_active:
            raise InvalidOperation(
                "Pricing rule is already inactive"
            )

        await (
            self._pricing_rule_repository
            .deactivate_pricing_rule(rule_id)
        )


    async def delete_pricing_rule(
        self,
        rule_id: int
    ) -> None:

        pricing_rule = await (
            self._pricing_rule_repository
            .get_pricing_rule_by_id(rule_id)
        )

        if not pricing_rule:
            raise ValueNotFound(
                "Pricing rule not found",
                {"rule_id": rule_id}
            )

        if pricing_rule.is_active:
            raise InvalidOperation(
                "Active pricing rules cannot be deleted"
            )

        await (
            self._pricing_rule_repository.delete_by_id(rule_id)
        )

    # =========================================================
    # PRODUCT PRICING
    # =========================================================

    async def assign_rule_to_product(
        self,
        product_id: int,
        rule_id: int
    ) -> None:

        rule = await self._pricing_rule_repository.get_pricing_rule_by_id(
            rule_id
        )

        if not rule:
            raise ValueNotFound(
                "Pricing rule not found",
                {"rule_id": rule_id}
            )

        await self._product_pricing_repository.assign_rule_to_product(
            product_id,
            rule_id
        )

    async def assign_rule_to_products(
        self,
        product_ids: list[int],
        rule_id: int
    ) -> None:

        rule = await self._pricing_rule_repository.get_pricing_rule_by_id(
            rule_id
        )

        if not rule:
            raise ValueNotFound(
                "Pricing rule not found",
                {"rule_id": rule_id}
            )

        await self._product_pricing_repository.assign_rule_to_products(
            product_ids,
            rule_id
        )

    async def remove_rule_from_product(
        self,
        product_id: int,
        rule_id: int
    ) -> None:

        await self._product_pricing_repository.remove_rule_from_product(
            product_id,
            rule_id
        )

    async def remove_rule_from_products(
        self,
        product_ids: list[int],
        rule_id: int
    ) -> None:

        await self._product_pricing_repository.remove_rule_from_products(
            product_ids,
            rule_id
        )

    async def get_product_pricing_detail(
        self,
        product_id: int
    ):

        detail = await (
            self._product_pricing_repository
            .get_product_pricing_detail(product_id)
        )

        if not detail:
            raise ValueNotFound(
                "Product pricing detail not found",
                {"product_id": product_id}
            )
        
        result = self._pricing_calculator.calculate(
            base_price=detail['base_price'],
            rules=detail['applied_rules']
        )

        detail["final_price"] = result.final_price
        detail["applied_rules"] = result.applied_rules

        return detail

    async def get_product_pricing_rules(
        self,
        product_id: int,
        *,
        limit: int = 20,
        page: int = 1
    ) -> dict:
        offset = self._pagination_service.get_offset(page, limit)

        pricing_rules = await (
            self._product_pricing_repository.get_pricing_rules_by_product_id(
                product_id=product_id,
                limit=limit,
                offset=offset
            )
        )

        total_items = await self._product_pricing_repository.count_pricing_rules_by_product_id(product_id)
        current_page = self._pagination_service.get_current_page(offset, limit)
        total_pages = self._pagination_service.get_total_pages(total_items, limit)

        return {
            "total_items": total_items,
            "items": pricing_rules,
            "pagination": {
                "current_page": current_page,
                "total_pages": total_pages
            }
        }

    async def get_products_pricing_summary(
        self,
        *,
        filter_command: FilterProductCommand,
        limit: int = 20,
        page: int = 1
    ):
        offset = self._pagination_service.get_offset(page, limit)
        
        products = await (
            self._product_pricing_repository
            .get_products_pricing_summary(
                limit=limit,
                offset=offset,
                name=filter_command.name,
                category=filter_command.categoria,
                brand=filter_command.marca
            )
        )

        if not products:
            return {
                "total_items": 0,
                "items": [],
                "pagination": {
                    "total_pages": 0,
                    "current_page": 1
                }
            }

        product_ids = [p['id'] for p in products]

        rules = await (
            self._product_pricing_repository
            .get_product_pricing_rules_summary(
                product_ids=product_ids
            )
        )

        # GROUP RULES BY PRODUCT

        rules_by_product: dict[int, list[ProductAppliedPricingRule]] = defaultdict(list)

        for rule in rules:
            rules_by_product[rule.product_id].append(rule)

        # BUILD RESPONSE

        result = []

        for product in products:
            product_rules: list[ProductAppliedPricingRule] = rules_by_product.get(product['id'], [])
            
            product: ProductPricingSummaryTD = dict(product)

            calculator_result = self._pricing_calculator.calculate(
                base_price=product["base_price"],
                rules=product_rules
            )

            product['final_price'] = calculator_result.final_price
            product['latest_applied_rule'] = calculator_result.latest_applied_rule

            result.append(product)

        total_items = await self._product_repository.count_filtered_products(filter_command)

        current_page = self._pagination_service.get_current_page(offset, limit)
        total_pages = self._pagination_service.get_total_pages(total_items, limit)

        return {
            "total_items": total_items,
            "items": result,
            "pagination": {
                "total_pages": total_pages,
                "current_page": current_page
            }
        }