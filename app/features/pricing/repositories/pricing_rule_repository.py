from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.dtos.pricing_rule_dto import PricingRuleSearchOptionDTO

from app.infra.db.repositories.base_repository import BaseRepository
from sqlalchemy import select, and_, func
from sqlmodel import col

class PricingRuleRepository(BaseRepository[PricingRule, PricingRuleTable]):
    async def get_pricing_rule_by_id(self, rule_id: int) -> PricingRule | None:
        return await self.get_by_id(rule_id)
    
    def _build_pricing_rule_conditions(
        self,
        *,
        type: str | None = None,
        search: str | None = None,
    ) -> list:
        
        conditions = []

        if type is not None:
            conditions.append(PricingRuleTable.type == type)

        if search:
            conditions.append(col(PricingRuleTable.name).ilike(f"%{search}%"))

        return conditions
    
    async def get_pricing_rules(
        self,
        *,
        type: str | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[PricingRule]:

        stmt = select(PricingRuleTable)

        conditions = self._build_pricing_rule_conditions(
            type=type,
            search=search,
        )

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.limit(limit).offset(offset)

        result = await self._db_session.execute(stmt)
        models = result.scalars().all()

        return [self._base_mapper.to_entity(m) for m in models]

    async def get_by_ids(
        self,
        *,
        rule_ids: list[int],
    ) -> list[PricingRule]:

        statement = (
            select(PricingRuleTable)
            .where(
                PricingRuleTable.id.in_(rule_ids)
            )
        )

        result = await self._db_session.execute(statement)

        models = result.scalars().all()

        return [
            self._base_mapper.to_entity(model)
            for model in models
        ]

    async def add_all(
        self,
        *,
        entities: list[PricingRule],
    ) -> list[PricingRule]:

        models = [
            self._base_mapper.to_db_model(entity)
            for entity in entities
        ]

        self._db_session.add_all(models)

        await self._db_session.flush()

        return [
            self._base_mapper.to_entity(model)
            for model in models
        ]

    async def search_options(
        self,
        search: str | None,
        offset: int,
        limit: int,
    ) -> list[PricingRuleSearchOptionDTO]:
        stmt = select(
            PricingRuleTable.id,
            PricingRuleTable.name,
            PricingRuleTable.description,
            PricingRuleTable.type,
            PricingRuleTable.parameters,
        )

        if search:
            search = search.strip()

            if search:
                pattern = f"%{search}%"

                stmt = stmt.where(
                    col(PricingRuleTable.name).ilike(pattern),
                )

        stmt = (
            stmt
            .order_by(
                col(PricingRuleTable.name).asc(),
                col(PricingRuleTable.id).asc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self._db_session.execute(stmt)

        return [
            PricingRuleSearchOptionDTO(
                id=row.id,
                name=row.name,
                description=row.description,
                type=row.type,
                parameters=row.parameters,
            )
            for row in result.all()
        ]

    async def count_search_options(
        self,
        search: str | None,
    ) -> int:
        stmt = select(
            func.count(PricingRuleTable.id)
        )

        if search:
            search = search.strip()

            if search:
                pattern = f"%{search}%"

                stmt = stmt.where(col(PricingRuleTable.name).ilike(pattern))

        result = await self._db_session.execute(stmt)

        return result.scalar_one()