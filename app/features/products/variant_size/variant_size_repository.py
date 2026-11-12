from app.features.products.variant_size.variant_size import VariantSize
from app.features.products.models.model_product import VariantSizeTable, ProductTable, VariantTable
from app.infra.db.repositories.base_repository import BaseRepository
from app.features.products.labels.dto import LabelDTO
from app.features.pricing.dtos.sale_pricing import SalePricingProductDTO

from sqlalchemy import select, Select
from sqlmodel import col

class VariantSizeRepository(
    BaseRepository[VariantSize, VariantSizeTable]
):
    async def get_label(
        self,
        variant_size_id: int,
    ) -> LabelDTO:
        stmt = self._label_query().where(
            VariantSizeTable.id == variant_size_id
        )

        row = (await self._db_session.execute(stmt)).one()

        return LabelDTO(
            variant_size_id=row.variant_size_id,
            product_name=row.nombre,
            barcode=row.barcode,
            base_price=row.base_price,
            brand_type=row.brand_type,
        )

    async def get_many_labels(
        self,
        variant_size_ids: list[int],
    ) -> list[LabelDTO]:
        stmt = self._label_query().where(
            VariantSizeTable.id.in_(variant_size_ids)
        )

        rows = (await self._db_session.execute(stmt)).all()

        return [
            LabelDTO(
                variant_size_id=row.variant_size_id,
                product_name=row.nombre,
                barcode=row.barcode,
                base_price=row.base_price,
                brand_type=row.brand_type,
            )
            for row in rows
        ]

    async def get_sale_pricing_products(
        self,
        variant_size_ids: list[int],
    ) -> list[SalePricingProductDTO]:
        stmt = (
            select(
                col(VariantSizeTable.id).label("variant_size_id"),
                ProductTable.base_price.label("unit_price"),
            )
            .join(
                VariantTable,
                VariantTable.id == VariantSizeTable.variant_id,
            )
            .join(
                ProductTable,
                ProductTable.id == VariantTable.product_id,
            )
            .where(
                VariantSizeTable.id.in_(variant_size_ids)
            )
        )

        rows = (await self._db_session.execute(stmt)).all()

        return [
            SalePricingProductDTO(
                variant_size_id=row.variant_size_id,
                unit_price=row.unit_price,
            )
            for row in rows
        ]

    def _label_query(self) -> Select:
        return (
            select(
                col(VariantSizeTable.id).label("variant_size_id"),
                ProductTable.nombre,
                VariantSizeTable.barcode,
                ProductTable.base_price,
                col(ProductTable.brand).label("brand_type"),
            )
            .join(
                VariantTable,
                VariantTable.id == VariantSizeTable.variant_id,
            )
            .join(
                ProductTable,
                ProductTable.id == VariantTable.product_id,
            )
        )

    