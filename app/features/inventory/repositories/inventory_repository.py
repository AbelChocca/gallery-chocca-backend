from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy import select, func, or_, Select, exists, update, and_, case
from sqlalchemy.orm import aliased

from app.core.exceptions import ValueNotFound
from app.features.inventory.entities.inventory import Inventory
from app.features.inventory.models.inventory import InventoryTable
from app.features.inventory.models.inventory_location import InventoryLocationTable
from app.infra.db.repositories.base_repository import BaseRepository
from app.features.products.models.model_product import ProductTable, VariantSizeTable, VariantTable
from app.features.inventory.types.inventory_movement import InventoryOwnerType
from app.features.material.models.model_material import MaterialTable
from app.features.material.types import MaterialType
from app.features.inventory.types.inventory import AvailabilityStatus

class InventoryRepository(
    BaseRepository[Inventory, InventoryTable],
):
    async def get_inventory_material_detail(
        self,
        *,
        material_id: int,
    ):

        inventory = aliased(
            InventoryTable
        )


        total_quantity = func.coalesce(
            func.sum(
                inventory.quantity
            ),
            Decimal("0")
        )


        total_reserved = func.coalesce(
            func.sum(
                inventory.reserved_quantity
            ),
            Decimal("0")
        )


        minimum_stock = func.coalesce(
            func.max(
                inventory.minimum_stock
            ),
            Decimal("0")
        )


        available_quantity = (
            total_quantity -
            total_reserved
        )


        availability_status = case(
            (
                available_quantity <= 0,
                AvailabilityStatus.OUT_OF_STOCK,
            ),
            (
                available_quantity <= minimum_stock,
                AvailabilityStatus.CRITICAL,
            ),
            else_=AvailabilityStatus.AVAILABLE,
        ).label(
            "availability_status"
        )


        statement = (
            select(
                MaterialTable.id.label(
                    "material_id"
                ),

                MaterialTable.code,
                MaterialTable.name,
                MaterialTable.description,

                MaterialTable.material_type,
                MaterialTable.unit_type,

                MaterialTable.company,
                MaterialTable.created_at,
                MaterialTable.updated_at,

                MaterialTable.is_active,


                total_quantity.label(
                    "total_quantity"
                ),

                total_reserved.label(
                    "total_reserved_quantity"
                ),

                available_quantity.label(
                    "total_available_quantity"
                ),

                minimum_stock.label(
                    "minimum_stock"
                ),

                availability_status,
            )
            .select_from(MaterialTable)
            .outerjoin(
                inventory,
                and_(
                    inventory.owner_id ==
                    MaterialTable.id,

                    inventory.owner_type ==
                    InventoryOwnerType.MATERIAL,
                )
            )
            .where(
                MaterialTable.id == material_id
            )
            .group_by(
                MaterialTable.id
            )
        )


        result = await self._db_session.execute(
            statement
        )


        material = result.mappings().one_or_none()

        if not material:
            raise ValueNotFound(
                "Material not found"
            )

        return material
    
    async def get_inventory_materials(
        self,
        *,
        current_location_id: int,
        offset: int = 0,
        limit: int = 20,
        search: str | None = None,
        material_type: MaterialType | None = None,
        availability_status: AvailabilityStatus | None = None,
        is_active: bool | None = None,
    ):

        (
            statement,
            available_quantity,
            minimum_stock_expr,
            current_inventory,
            quantity,
            reserved_quantity,
        ) = self._build_inventory_materials_query(
            current_location_id=current_location_id,
            search=search,
            material_type=material_type,
            is_active=is_active,
        )


        if availability_status:
            statement = statement.having(
                self._availability_filter(
                    availability_status,
                    available_quantity,
                    minimum_stock_expr,
                )
            )


        statement = (
            statement
            .group_by(
                MaterialTable.id,
                MaterialTable.code,
                MaterialTable.name,
                MaterialTable.material_type,
                MaterialTable.unit_type,
                MaterialTable.is_active,
                quantity,
                reserved_quantity,
                minimum_stock_expr,
            )
            .order_by(
                MaterialTable.name.asc()
            )
            .offset(offset)
            .limit(limit)
        )


        result = await self._db_session.execute(
            statement
        )

        return result.all()

    async def get_inventory_materials_count(
        self,
        *,
        current_location_id: int,
        search: str | None = None,
        material_type: MaterialType | None = None,
        availability_status: AvailabilityStatus | None = None,
        is_active: bool | None = None,
    ):

        (
            statement,
            available_quantity,
            minimum_stock_expr,
            current_inventory,
            quantity,
            reserved_quantity,
        ) = self._build_inventory_materials_query(
            current_location_id=current_location_id,
            search=search,
            material_type=material_type,
            is_active=is_active,
        )


        statement = statement.with_only_columns(
            MaterialTable.id
        )


        if availability_status:
            statement = (
                statement
                .having(
                    self._availability_filter(
                        availability_status,
                        available_quantity,
                        minimum_stock_expr,
                    )
                )
            )


        filtered_query = (
            statement
            .group_by(
                MaterialTable.id,
                MaterialTable.code,
                MaterialTable.name,
                MaterialTable.material_type,
                MaterialTable.unit_type,
                MaterialTable.is_active,
                quantity,
                reserved_quantity,
                minimum_stock_expr,
            )
            .subquery()
        )


        count_statement = select(
            func.count()
        ).select_from(
            filtered_query
        )


        result = await self._db_session.execute(
            count_statement
        )

        return result.scalar_one()
        
    async def get_by_owner_location(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
        location_id: int,
        raises: bool = True,
    ) -> Inventory:

        statement = select(
            InventoryTable
        ).where(
            InventoryTable.owner_type == owner_type,
            InventoryTable.owner_id == owner_id,
            InventoryTable.location_id == location_id,
        )

        result = await self._db_session.execute(statement)

        inventory_table = result.scalar_one_or_none()

        if inventory_table is None:
            if raises:
                raise ValueNotFound("Inventory not found.")
            return None

        return self._base_mapper.to_entity(inventory_table)

    async def update_stock(
        self,
        *,
        inventory_id: int,
        new_stock: Decimal,
    ) -> None:

        statement = (
            update(InventoryTable)
            .where(
                InventoryTable.id == inventory_id
            )
            .values(
                quantity=new_stock,
                last_movement_at=datetime.now(timezone.utc),
            )
        )

        await self._db_session.execute(statement)

    async def update_stock_many(
        self,
        stock_updates: dict[int, dict[str, Decimal]]
    ):

        quantity_case = case(
            {
                inventory_id: values["quantity"]
                for inventory_id, values in stock_updates.items()
            },
            value=InventoryTable.id
        )


        await self._db_session.execute(
            update(InventoryTable)
            .where(
                InventoryTable.id.in_(
                    stock_updates.keys()
                )
            )
            .values(
                quantity=quantity_case
            )
        )

    async def get_inventory_product_detail(
        self,
        *,
        variant_size_id: int,
    ):

        statement = (
            select(
                VariantSizeTable.id.label("variant_size_id"),
                VariantTable.id.label("variant_id"),

                ProductTable.nombre,
                VariantTable.color,

                VariantSizeTable.size,
                VariantSizeTable.sku,
                VariantSizeTable.barcode,

                InventoryTable.id.label("inventory_id"),

                InventoryTable.quantity,
                InventoryTable.reserved_quantity,
                InventoryTable.minimum_stock,

                InventoryTable.last_movement_at,

                InventoryLocationTable.id.label("location_id"),
                InventoryLocationTable.name.label("location_name"),
                InventoryLocationTable.type.label("location_type"),
                InventoryLocationTable.address.label("location_address"),
            )
            .join(
                VariantTable,
                VariantTable.id == VariantSizeTable.variant_id,
            )
            .join(
                ProductTable,
                ProductTable.id == VariantTable.product_id,
            )
            .outerjoin(
                InventoryTable,
                and_(
                    InventoryTable.owner_id == VariantSizeTable.id,
                    InventoryTable.owner_type == InventoryOwnerType.PRODUCT,
                ),
            )
            .outerjoin(
                InventoryLocationTable,
                InventoryLocationTable.id == InventoryTable.location_id,
            )
            .where(
                VariantSizeTable.id == variant_size_id
            )
        )

        result = await self._db_session.execute(statement)

        return result.all()

    async def get_inventory_owner_locations(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
    ):
        
        statement = (
            select(
                InventoryTable.id.label(
                    "inventory_id"
                ),

                InventoryTable.owner_id,
                InventoryTable.owner_type,

                InventoryTable.location_id,

                InventoryTable.quantity,
                InventoryTable.reserved_quantity,
                InventoryTable.minimum_stock,

                InventoryTable.last_movement_at,


                InventoryLocationTable.name.label(
                    "location_name"
                ),

                InventoryLocationTable.type.label(
                    "location_type"
                ),

                InventoryLocationTable.address.label(
                    "location_address"
                ),
            )
            .outerjoin(
                InventoryLocationTable,
                InventoryLocationTable.id ==
                InventoryTable.location_id,
            )
            .where(
                InventoryTable.owner_id == owner_id,

                InventoryTable.owner_type == owner_type,
            )
        )


        result = await self._db_session.execute(
            statement
        )

        return result.all()
        
    async def get_owner_inventories(
        self,
        *,
        owner_id: int,
        owner_type: InventoryOwnerType
    ) -> list[Inventory]:

        statement = (
            select(InventoryTable)
            .where(
                InventoryTable.owner_id == owner_id,
                InventoryTable.owner_type == owner_type
            )
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]

    async def get_owner_inventories_many(
        self,
        *,
        owner_ids: list[int],
        owner_type: InventoryOwnerType
    ) -> list[Inventory]:

        statement = (
            select(InventoryTable)
            .where(
                InventoryTable.owner_id.in_(owner_ids),
                InventoryTable.owner_type == owner_type
            )
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]
    
    async def update_minimum_stock(
        self,
        *,
        inventory_id: int,
        minimum_stock: Decimal,
    ) -> Inventory:

        stmt = (
            update(InventoryTable)
            .where(
                InventoryTable.id == inventory_id
            )
            .values(
                minimum_stock=minimum_stock
            )
        )

        await self._db_session.execute(stmt)

    async def get_inventory_products_count(
        self,
        *,
        search: str | None = None,
        colors: list[str] | None = None,
        size: str | None = None,
    ) -> int:

        statement = (
            select(
                func.count(VariantSizeTable.id)
            )
            .select_from(VariantSizeTable)
            .join(
                VariantTable,
                VariantTable.id == VariantSizeTable.variant_id,
            )
            .join(
                ProductTable,
                ProductTable.id == VariantTable.product_id,
            )
        )

        if search:
            normalized_search = f"%{search}%"

            statement = statement.where(
                or_(
                    func.unaccent(ProductTable.nombre).ilike(
                        func.unaccent(normalized_search)
                    ),
                    VariantSizeTable.sku.ilike(normalized_search),
                    VariantSizeTable.barcode.ilike(normalized_search),
                )
            )

        if colors:
            statement = statement.where(
                VariantTable.color.in_(colors)
            )

        if size:
            statement = statement.where(
                VariantSizeTable.size == size
            )

        result = await self._db_session.execute(statement)

        return result.scalar_one()
    
    async def get_other_locations_stock(
        self,
        *,
        owner_ids: list[int],
        owner_type: InventoryOwnerType,
        current_location_id: int,
    ):
        
        statement = (
            select(
                InventoryTable.owner_id,
                func.coalesce(
                    func.sum(
                        InventoryTable.quantity
                    ),
                    0,
                ).label(
                    "available_quantity"
                ),
            )
            .where(
                InventoryTable.owner_id.in_(owner_ids),
                InventoryTable.owner_type == owner_type,
                InventoryTable.location_id != current_location_id,
            )
            .group_by(
                InventoryTable.owner_id
            )
        )

        result = await self._db_session.execute(statement)

        return {
            row.owner_id: row.available_quantity
            for row in result.all()
        }
    
    async def get_inventory_products(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        search: str | None = None,
        colors: list[str] | None = None,
        size: str | None = None,
    ):
        statement: Select = (
            select(
                VariantSizeTable.id.label("variant_size_id"),
                VariantTable.id.label("variant_id"),

                ProductTable.nombre,

                VariantTable.color,

                VariantSizeTable.size,
                VariantSizeTable.sku,
                VariantSizeTable.barcode,

                func.coalesce(
                    func.sum(
                        InventoryTable.minimum_stock
                    ),
                    0,
                ).label("total_minimum_stock"),

                func.coalesce(
                    func.sum(
                        InventoryTable.quantity
                    ),
                    0,
                ).label("total_quantity"),

                func.coalesce(
                    func.sum(
                        InventoryTable.reserved_quantity
                    ),
                    0,
                ).label("reserved_quantity"),
            )
            .outerjoin(
                InventoryTable,
                and_(
                    InventoryTable.owner_id == VariantSizeTable.id,
                    InventoryTable.owner_type == InventoryOwnerType.PRODUCT,
                ),
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

        if search:
            normalized_search = f"%{search}%"

            statement = statement.where(
                or_(
                    func.unaccent(ProductTable.nombre).ilike(
                        func.unaccent(normalized_search)
                    ),
                    VariantSizeTable.sku.ilike(normalized_search),
                    VariantSizeTable.barcode.ilike(normalized_search),
                )
            )

        if colors:
            statement = statement.where(
                VariantTable.color.in_(colors)
            )

        if size:
            statement = statement.where(
                VariantSizeTable.size == size
            )

        statement = (
            statement
            .group_by(
                VariantSizeTable.id,
                VariantTable.id,
                ProductTable.nombre,
                VariantTable.color,
                VariantSizeTable.size,
                VariantSizeTable.sku,
                VariantSizeTable.barcode,
            )
            .order_by(
                ProductTable.nombre.asc(),
                VariantTable.color.asc(),
                VariantSizeTable.size.asc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self._db_session.execute(statement)

        return result.all()
    
    async def has_stock_in_location(
        self,
        *,
        location_id: int,
    ) -> bool:

        statement = select(
            exists().where(
                InventoryTable.location_id == location_id,
                InventoryTable.quantity > Decimal("0"),
            )
        )

        result = await self._db_session.execute(statement)

        return result.scalar()

    def _build_inventory_materials_query(
        self,
        *,
        current_location_id: int | None = None,
        search: str | None = None,
        material_type: MaterialType | None = None,
        is_active: bool | None = None,
    ):
        current_inventory = aliased(InventoryTable)
        total_inventory = aliased(InventoryTable)

        total_quantity = func.coalesce(
            func.sum(total_inventory.quantity),
            Decimal("0"),
        )

        quantity = func.coalesce(
            current_inventory.quantity,
            Decimal("0"),
        )

        reserved_quantity = func.coalesce(
            current_inventory.reserved_quantity,
            Decimal("0"),
        )

        available_quantity = (
            quantity - reserved_quantity
        )

        minimum_stock_expr = func.coalesce(
            current_inventory.minimum_stock,
            Decimal("0"),
        )

        minimum_stock = minimum_stock_expr.label(
            "minimum_stock"
        )

        availability_status = case(
            (
                available_quantity <= 0,
                AvailabilityStatus.OUT_OF_STOCK,
            ),
            (
                available_quantity <= minimum_stock,
                AvailabilityStatus.CRITICAL,
            ),
            else_=AvailabilityStatus.AVAILABLE,
        ).label(
            "availability_status"
        )


        statement = (
            select(
                MaterialTable.id.label("material_id"),

                MaterialTable.code,
                MaterialTable.name,
                MaterialTable.material_type,
                MaterialTable.unit_type,
                MaterialTable.is_active,

                minimum_stock,

                total_quantity.label(
                    "total_quantity"
                ),

                reserved_quantity.label(
                    "reserved_quantity"
                ),

                available_quantity.label(
                    "available_quantity"
                ),

                availability_status,
            )
            .select_from(MaterialTable)
        )


        if current_location_id is not None:

            statement = statement.outerjoin(
                current_inventory,
                and_(
                    current_inventory.owner_type ==
                    InventoryOwnerType.MATERIAL,

                    current_inventory.owner_id ==
                    MaterialTable.id,

                    current_inventory.location_id ==
                    current_location_id,
                ),
            )


        statement = statement.outerjoin(
            total_inventory,
            and_(
                total_inventory.owner_type ==
                InventoryOwnerType.MATERIAL,

                total_inventory.owner_id ==
                MaterialTable.id,
            ),
        )


        if search:
            normalized_search = func.unaccent(
                f"%{search}%"
            )

            statement = statement.where(
                or_(
                    func.unaccent(MaterialTable.code)
                    .ilike(normalized_search),

                    func.unaccent(MaterialTable.name)
                    .ilike(normalized_search),
                )
            )


        if material_type:
            statement = statement.where(
                MaterialTable.material_type ==
                material_type
            )


        if is_active is not None:
            statement = statement.where(
                MaterialTable.is_active ==
                is_active
            )


        return (
            statement,
            available_quantity,
            minimum_stock_expr,
            current_inventory,
            quantity,
            reserved_quantity,
        )

    def _availability_filter(
        self,
        status: AvailabilityStatus,
        available_quantity,
        minimum_stock,
    ):

        if status == AvailabilityStatus.OUT_OF_STOCK:
            return available_quantity <= 0


        if status == AvailabilityStatus.CRITICAL:
            return and_(
                available_quantity > 0,
                available_quantity <= minimum_stock,
            )


        if status == AvailabilityStatus.AVAILABLE:
            return available_quantity > minimum_stock