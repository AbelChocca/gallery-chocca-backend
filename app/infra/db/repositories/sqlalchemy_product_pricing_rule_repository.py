from sqlalchemy import select, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from app.features.products.models.model_product import ProductTable, VariantTable
from app.infra.db.models.model_product_pricing_rule import (
    ProductPricingRuleTable
)
from app.infra.db.models.model_pricing_rule import PricingRuleTable
from app.infra.db.models.model_media import MediaImageTable

from app.features.pricing.entities.product_applied_pricing_rule import ProductAppliedPricingRule
from app.infra.db.mappers.pricing_rule_mapper import PricingRuleMapper
from app.features.pricing.types import ProductPricingSummaryTD
from app.features.media.types import ImageType

class ProductPricingRepository:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_product_base_price(self, product_id: int):
        stmt = (
            select(ProductTable.base_price)
            .where(ProductTable.id == product_id)
        )

        result = await self._db_session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def count_pricing_rules_by_product_id(
        self,
        product_id: int
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(ProductPricingRuleTable)
            .where(
                ProductPricingRuleTable.product_id == product_id
            )
        )

        result = await self._db_session.execute(stmt)

        return result.scalar_one()
    
    async def update_product_base_price(self, product_id: int, base_price: int) -> None:
        stmt = (
            select(ProductTable)
            .where(ProductTable.id == product_id)
        )

        result = await self._db_session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            return None

        product.base_price = base_price

        await self._db_session.flush()

    async def assign_rule_to_product(self, product_id: int, rule_id: int):
        model = ProductPricingRuleTable(
            product_id=product_id,
            pricing_rule_id=rule_id
        )

        self._db_session.add(model)
    
    async def assign_rule_to_products(self, product_ids: list[int], rule_id: int):
        models = [
            ProductPricingRuleTable(
                product_id=pid,
                pricing_rule_id=rule_id
            )
            for pid in product_ids
        ]

        self._db_session.add_all(models)

    async def remove_rule_from_product(self, product_id: int, rule_id: int):
        stmt = delete(ProductPricingRuleTable).where(
            ProductPricingRuleTable.product_id == product_id,
            ProductPricingRuleTable.pricing_rule_id == rule_id
        )

        await self._db_session.execute(stmt)

    async def remove_rule_from_products(self, product_ids: list[int], rule_id: int):
        stmt = delete(ProductPricingRuleTable).where(
            ProductPricingRuleTable.pricing_rule_id == rule_id,
            col(ProductPricingRuleTable.product_id).in_(product_ids)
        )

        await self._db_session.execute(stmt)
    
    async def get_products_pricing_summary(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        name: str | None = None,
        category: str | None = None,
        brand: str | None = None
    ) -> list[ProductPricingSummaryTD]:
        primary_image_subq = (
            select(MediaImageTable.image_url)
            .join(
                VariantTable,
                VariantTable.id == MediaImageTable.owner_id
            )
            .where(
                VariantTable.product_id == ProductTable.id,
                MediaImageTable.owner_type == ImageType.variant,
                col(MediaImageTable.is_primary).is_(True)
            )
            .limit(1)
            .scalar_subquery()
        )

        stmt_products = (
            select(
                ProductTable.id,
                ProductTable.nombre,
                ProductTable.categoria,
                ProductTable.base_price,
                ProductTable.is_active,
                primary_image_subq.label("image_url"),
            )
        )

        conditions = []

        if name:
            conditions.append(
                ProductTable.nombre.ilike(f"%{name}%")
            )

        if category:
            conditions.append(
                ProductTable.categoria == category
            )

        if brand:
            conditions.append(
                ProductTable.marca == brand
            )

        if conditions:
            stmt_products = stmt_products.where(and_(*conditions))

        stmt_products = (
            stmt_products
            .limit(limit)
            .offset(offset)
        )

        products_result = await self._db_session.execute(stmt_products)

        return products_result.mappings().all()

    async def get_product_pricing_rules_summary(self, product_ids: list[int]) -> list[ProductAppliedPricingRule]:
        stmt_rules = (
            select(
                ProductPricingRuleTable.product_id,
                ProductPricingRuleTable.assigned_at,
                PricingRuleTable
            )
            .join(
                PricingRuleTable,
                PricingRuleTable.id == ProductPricingRuleTable.pricing_rule_id
            )
            .where(
                col(ProductPricingRuleTable.product_id).in_(product_ids)
            )
            .order_by(
                col(ProductPricingRuleTable.assigned_at).desc()
            )
        )

        result = await self._db_session.execute(stmt_rules)

        rows = result.all()

        return self._parse_applied_pricing_rules(rows)
    
    async def get_product_pricing_detail(
            self, 
            product_id: int,
        ) -> ProductPricingSummaryTD:
        stmt_product = (
            select(
                ProductTable.id,
                ProductTable.nombre,
                ProductTable.categoria,
                ProductTable.base_price,
                ProductTable.is_active,
                MediaImageTable.image_url,
            )
            .join(VariantTable, VariantTable.product_id == ProductTable.id)
            .join(
                MediaImageTable,
                and_(
                    MediaImageTable.owner_id == VariantTable.id,
                    MediaImageTable.owner_type == ImageType.variant,
                    col(MediaImageTable.is_primary).is_(True)
                )
            )
            .where(ProductTable.id == product_id)
        )

        product_result = await self._db_session.execute(stmt_product)

        product = product_result.mappings().first()

        if not product:
            return None
        
        stmt_rules = (
            self._build_product_pricing_rules_stmt(product_id, active_rules=True)
            .order_by(
                col(ProductPricingRuleTable.assigned_at).desc()
            )
        )
        
        rules_result = await self._db_session.execute(stmt_rules)

        rows = rules_result.all()

        pricing_rules = self._parse_applied_pricing_rules(
            rows
        )

        product: ProductPricingSummaryTD = dict(product)

        product['applied_rules'] = pricing_rules

        return product
        
    async def get_pricing_rules_by_product_id(
        self,
        product_id: int,
        *,
        limit: int = 20,
        offset: int = 0
    ) -> list[ProductAppliedPricingRule]:
        stmt = self._build_product_pricing_rules_stmt(
            product_id
        )

        stmt = (
            stmt
            .order_by(
                col(ProductPricingRuleTable.assigned_at).desc()
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self._db_session.execute(stmt)

        rows = result.all()

        return self._parse_applied_pricing_rules(
            rows
        )
    
    def _build_product_pricing_rules_stmt(
        self,
        product_id: int,
        *,
        active_rules: bool | None = None
    ):
        conditions = [
            ProductPricingRuleTable.product_id == product_id
        ]

        if active_rules is not None:
            conditions.append(
                PricingRuleTable.is_active == active_rules
            )

        return (
            select(
                ProductPricingRuleTable.product_id,
                ProductPricingRuleTable.assigned_at,
                PricingRuleTable
            )
            .select_from(ProductPricingRuleTable)
            .join(
                PricingRuleTable,
                PricingRuleTable.id == ProductPricingRuleTable.pricing_rule_id
            )
            .where(and_(*conditions))
        )
    
    def _parse_applied_pricing_rules(
        self,
        rows
    ) -> list[ProductAppliedPricingRule]:

        applied_rules: list[dict] = []

        for product_id, assigned_at, rule_model in rows:

            pricing_rule = PricingRuleMapper.to_entity(
                rule_model
            )

            applied_rule = ProductAppliedPricingRule(
                product_id=product_id,
                pricing_rule=pricing_rule,
                assigned_at=assigned_at
            )

            applied_rules.append(applied_rule)

        return applied_rules