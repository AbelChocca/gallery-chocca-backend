from app.features.inventory.repositories.sqlalchemy_inventory_movement_repo import PostgresInventoryMovementReposity
from app.infra.db.mappers.inventory_movement_mapper import InventoryMovementMapper
from app.features.inventory.models.inventory_movement import InventoryMovementTable

from app.infra.db.repositories.product_repository import PostgresProductRepository
from app.infra.db.mappers.product_mapper import ProductMapper
from app.features.products.models.model_product import ProductTable, VariantSizeTable, VariantTable

from app.infra.db.repositories.sqlmodel_slide_repository import PostgresSlideRepository
from app.infra.db.mappers.slide_mapper import SlideMapper
from app.infra.db.models.model_slide import SlideTable

from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.db.mappers.image_mapper import ImageMapper
from app.infra.db.models.model_media import MediaImageTable

from app.infra.db.repositories.sqlalchemy_user_repository import PostgresUserRepository
from app.infra.db.mappers.user_mapper import UserMapper
from app.infra.db.models.model_user import UserTable

from app.infra.db.repositories.sqlmodel_favorites_repository import PostgresFavoritesRepository
from app.infra.db.mappers.favorite_mapper import FavoritesMapper
from app.infra.db.models.model_favorites import FavoritesTable

from app.infra.db.repositories.sqlalchemy_cart_repository import CartRepository
from app.infra.db.mappers.cart_mapper import CartMapper
from app.infra.db.models.model_cart import CartTable

from app.infra.db.repositories.sqlalchemy_pricing_rule_repository import PricingRuleRepository
from app.infra.db.mappers.pricing_rule_mapper import PricingRuleMapper
from app.infra.db.models.model_pricing_rule import PricingRuleTable

from app.infra.db.repositories.sqlalchemy_product_pricing_rule_repository import ProductPricingRepository

from app.features.material.material_repository import PostgresMaterialRepository
from app.infra.db.mappers.material_mapper import MaterialMapper
from app.features.material.models.model_material import MaterialTable

from app.infra.db.repositories.variant_repository import VariantRepository
from app.infra.db.repositories.variant_size_repository import VariantSizeRepository

from app.infra.db.mappers.variant_mapper import VariantMapper
from app.infra.db.mappers.variant_size_mapper import VariantSizeMapper

from app.features.inventory.repositories.inventory_repository import InventoryRepository
from app.features.inventory.models.inventory import InventoryTable
from app.features.inventory.mappers.inventory_mapper import InventoryMapper

from app.features.inventory.mappers.inventory_location import (
    InventoryLocationMapper,
)
from app.features.inventory.repositories.inventory_location_repository import (
    InventoryLocationRepository,
)
from app.features.inventory.models.inventory_location import (
    InventoryLocationTable,
)

from app.features.balancing.repositories.balance_snapshot_repository import BalanceSnapshotRepository
from app.features.balancing.mappers.balance_snapshot_mapper import BalanceSnapshotMapper
from app.features.balancing.models.balance_snapshot import BalanceSnapshotTable

from app.features.balancing.repositories.accounts_receivable_repository import (
    AccountsReceivableRepository,
)

from app.features.balancing.repositories.accounts_payable_repository import (
    AccountsPayableRepository,
)

from app.features.balancing.repositories.financial_debt_repository import (
    FinancialDebtRepository,
)

from app.features.balancing.repositories.inventory_valuation_repository import (
    InventoryValuationRepository,
)

from app.features.balancing.repositories.other_current_liability_repository import (
    OtherCurrentLiabilityRepository,
)


from app.features.balancing.mappers.accounts_receivable_mapper import (
    AccountsReceivableMapper,
)

from app.features.balancing.mappers.accounts_payable_mapper import (
    AccountsPayableMapper,
)

from app.features.balancing.mappers.financial_debt_mapper import (
    FinancialDebtMapper,
)

from app.features.balancing.mappers.inventory_valuation_mapper import (
    InventoryValuationMapper,
)

from app.features.balancing.mappers.other_current_liability_mapper import (
    OtherCurrentLiabilityMapper,
)


from app.features.balancing.models.accounts_receivable import (
    AccountsReceivableTable,
)

from app.features.balancing.models.accounts_payable import (
    AccountsPayableTable,
)

from app.features.balancing.models.financial_debt import (
    FinancialDebtTable,
)

from app.features.balancing.models.inventory_valuation import (
    InventoryValuationTable,
)

from app.features.balancing.models.other_current_liability import (
    OtherCurrentLiabilityTable,
)

from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import AbstractAsyncContextManager
from typing import Callable, Type, TypeVar

T = TypeVar("T")

class UnitOfWork(AbstractAsyncContextManager):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

        self._repositories = None

    @property
    def accounts_receivable(
        self,
    ) -> AccountsReceivableRepository:

        return self._get_or_create(
            "accounts_receivable",
            lambda: AccountsReceivableRepository(
                self.session,
                AccountsReceivableMapper,
                AccountsReceivableTable,
            ),
        )

    @property
    def accounts_payable(
        self,
    ) -> AccountsPayableRepository:

        return self._get_or_create(
            "accounts_payable",
            lambda: AccountsPayableRepository(
                self.session,
                AccountsPayableMapper,
                AccountsPayableTable,
            ),
        )

    @property
    def financial_debts(
        self,
    ) -> FinancialDebtRepository:

        return self._get_or_create(
            "financial_debts",
            lambda: FinancialDebtRepository(
                self.session,
                FinancialDebtMapper,
                FinancialDebtTable,
            ),
        )

    @property
    def inventory_valuations(
        self,
    ) -> InventoryValuationRepository:

        return self._get_or_create(
            "inventory_valuations",
            lambda: InventoryValuationRepository(
                self.session,
                InventoryValuationMapper,
                InventoryValuationTable,
            ),
        )

    @property
    def other_current_liabilities(
        self,
    ) -> OtherCurrentLiabilityRepository:

        return self._get_or_create(
            "other_current_liabilities",
            lambda: OtherCurrentLiabilityRepository(
                self.session,
                OtherCurrentLiabilityMapper,
                OtherCurrentLiabilityTable,
            ),
        )

    @property
    def balance_snapshots(self) -> BalanceSnapshotRepository:
        return self._get_or_create(
            "balance_snapshots",
            lambda: BalanceSnapshotRepository(
                self.session,
                BalanceSnapshotMapper,
                BalanceSnapshotTable,
            ),
        )
    
    @property
    def favorites(
        self
    ) -> PostgresFavoritesRepository:

        return self._get_or_create(
            "favorites",
            lambda: PostgresFavoritesRepository(
                self.session,
                FavoritesMapper,
                FavoritesTable
            )
        )


    @property
    def images(
        self
    ) -> PostgresImageRepository:

        return self._get_or_create(
            "images",
            lambda: PostgresImageRepository(
                self.session,
                ImageMapper,
                MediaImageTable
            )
        )

    @property
    def inventory(
        self
    ) -> InventoryRepository:
        return self._get_or_create(
            "inventory",
            lambda: InventoryRepository(
                self.session,
                InventoryMapper,
                InventoryTable
            )
        )

    @property
    def inventory_movements(
        self
    ) -> PostgresInventoryMovementReposity:

        return self._get_or_create(
            "inventory_movements",
            lambda: PostgresInventoryMovementReposity(
                self.session,
                InventoryMovementMapper,
                InventoryMovementTable
            )
        )


    @property
    def carts(
        self
    ) -> CartRepository:

        return self._get_or_create(
            "carts",
            lambda: CartRepository(
                self.session,
                CartMapper,
                CartTable
            )
        )

    @property
    def inventory_locations(
        self,
    ) -> InventoryLocationRepository:

        return self._get_or_create(
            "inventory_locations",
            lambda: InventoryLocationRepository(
                self.session,
                InventoryLocationMapper,
                InventoryLocationTable,
            ),
        )

    @property
    def pricing_rules(
        self
    ) -> PricingRuleRepository:

        return self._get_or_create(
            "pricing_rules",
            lambda: PricingRuleRepository(
                self.session,
                PricingRuleMapper,
                PricingRuleTable
            )
        )


    @property
    def product_pricing(
        self
    ) -> ProductPricingRepository:

        return self._get_or_create(
            "product_pricing",
            lambda: ProductPricingRepository(
                self.session
            )
        )


    @property
    def materials(
        self
    ) -> PostgresMaterialRepository:

        return self._get_or_create(
            "materials",
            lambda: PostgresMaterialRepository(
                self.session,
                MaterialMapper,
                MaterialTable
            )
        )
    
    @property
    def products(
        self
    ) -> PostgresProductRepository:

        return self._get_or_create(
            "products",
            lambda: PostgresProductRepository(
                self.session,
                ProductMapper,
                ProductTable
            )
        )
    
    @property
    def variants(
        self,
    ) -> VariantRepository:

        return self._get_or_create(
            "variants",
            lambda: VariantRepository(
                self.session,
                VariantMapper,
                VariantTable,
            ),
        )

    @property
    def variant_sizes(
        self,
    ) -> VariantSizeRepository:

        return self._get_or_create(
            "variant_sizes",
            lambda: VariantSizeRepository(
                self.session,
                VariantSizeMapper,
                VariantSizeTable,
            ),
        )
    
    @property
    def slides(
        self
    ) -> PostgresSlideRepository:

        return self._get_or_create(
            "slides",
            lambda: PostgresSlideRepository(
                self.session,
                SlideMapper,
                SlideTable
            )
        )
    
    @property
    def users(
        self
    ) -> PostgresUserRepository:

        return self._get_or_create(
            "users",
            lambda: PostgresUserRepository(
                self.session,
                UserMapper,
                UserTable
            )
        )
    
    def _get_or_create(
        self,
        key: str,
        factory: Callable[[], T]
    ) -> T:
        if key not in self._repositories:
            self._repositories[key] = factory()

        return self._repositories[key]
    
    async def __aenter__(self) -> "UnitOfWork":
        if self.session is not None:
            await self.session.close()
            
        self.session = self._session_factory()
        self._repositories = {}

        return self

    async def __aexit__(self, exc_type: Type[BaseException], exc, tb):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close() 
            self.session = None
            self._repositories = None
