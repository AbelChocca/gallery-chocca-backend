from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.infra.db.exceptions import DatabaseException
from app.infra.db.repositories.base_repository import BaseRepository

from app.features.balancing.entities.inventory_valuation import (
    InventoryValuation,
)
from app.features.balancing.models.inventory_valuation import (
    InventoryValuationTable,
)
from app.features.balancing.types.inventory_valuation_types import (
    InventoryValuationCategory,
)


class InventoryValuationRepository(
    BaseRepository[
        InventoryValuation,
        InventoryValuationTable,
    ]
):

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        category: InventoryValuationCategory | None = None,
        subcategory: str | None = None,
        brand: str | None = None,
        location: str | None = None,
    ) -> list[InventoryValuation]:

        try:
            statement = select(InventoryValuationTable)

            if balance_snapshot_id is not None:
                statement = statement.where(
                    InventoryValuationTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if category is not None:
                statement = statement.where(
                    InventoryValuationTable.category == category
                )

            if subcategory is not None:
                statement = statement.where(
                    InventoryValuationTable.subcategory == subcategory
                )

            if brand is not None:
                statement = statement.where(
                    InventoryValuationTable.brand == brand
                )

            if location is not None:
                statement = statement.where(
                    InventoryValuationTable.location == location
                )

            statement = statement.order_by(
                InventoryValuationTable.created_at.desc()
            )

            result = await self._db_session.execute(statement)

            models = result.scalars().all()

            return [
                self._base_mapper.to_entity(model)
                for model in models
            ]

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while getting inventory valuations.",
                {
                    "repository": "postgres_inventoryvaluation",
                    "base_model": InventoryValuationTable.__name__,
                    "event": "find",
                    "balance_snapshot_id": balance_snapshot_id,
                    "category": category.value if category else None,
                    "subcategory": subcategory,
                    "brand": brand,
                    "location": location,
                    "original_error": str(getattr(s, "orig", s)),
                },
            ) from s

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        category: InventoryValuationCategory | None = None,
        subcategory: str | None = None,
        brand: str | None = None,
        location: str | None = None,
    ) -> Decimal:

        try:
            statement = select(
                func.coalesce(
                    func.sum(
                        InventoryValuationTable.quantity
                        * InventoryValuationTable.unit_value
                    ),
                    0,
                )
            )

            if balance_snapshot_id is not None:
                statement = statement.where(
                    InventoryValuationTable.balance_snapshot_id
                    == balance_snapshot_id
                )

            if category is not None:
                statement = statement.where(
                    InventoryValuationTable.category == category
                )

            if subcategory is not None:
                statement = statement.where(
                    InventoryValuationTable.subcategory == subcategory
                )

            if brand is not None:
                statement = statement.where(
                    InventoryValuationTable.brand == brand
                )

            if location is not None:
                statement = statement.where(
                    InventoryValuationTable.location == location
                )

            result = await self._db_session.execute(statement)

            return result.scalar_one()

        except SQLAlchemyError as s:
            raise DatabaseException(
                "Postgres error while calculating inventory valuation total.",
                {
                    "repository": "postgres_inventoryvaluation",
                    "base_model": InventoryValuationTable.__name__,
                    "event": "sum_amount",
                    "balance_snapshot_id": balance_snapshot_id,
                    "category": category.value if category else None,
                    "subcategory": subcategory,
                    "brand": brand,
                    "location": location,
                    "original_error": str(getattr(s, "orig", s)),
                },
            ) from s