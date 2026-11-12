from app.features.inventory.repositories.sqlalchemy_inventory_movement_repo import PostgresInventoryMovementReposity
from app.infra.db.mappers.inventory_movement_mapper import InventoryMovementMapper
from app.features.inventory.models.inventory_movement import InventoryMovementTable

from app.features.products.product_repository import PostgresProductRepository
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

from app.features.cart.cart_repository import CartRepository
from app.infra.db.mappers.cart_mapper import CartMapper
from app.infra.db.models.model_cart import CartTable

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

from app.infra.db.uow.repositories.pricing import PricingRepositoriesMixin
from app.infra.db.uow.repositories.customer import CustomerRepositoriesMixin
from app.infra.db.uow.repositories.order import (
    OrdersRepositoriesMixin,
)
from app.infra.db.uow.repositories.complaints import ComplaintsRepositoriesMixin
from app.infra.db.uow.repositories.payment import PaymentsRepositoriesMixin
from app.infra.db.uow.repositories.balancing import (
    BalancingRepositoriesMixin,
)

from app.features.consents.consent_repository import (
    UserConsentRepository,
)
from app.features.consents.user_consent_mapper import (
    UserConsentMapper,
)
from app.features.consents.models.user_consent import (
    UserConsentTable,
)


from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import AbstractAsyncContextManager
from typing import Callable, Type, TypeVar

T = TypeVar("T")

class UnitOfWork(
    PricingRepositoriesMixin,
    CustomerRepositoriesMixin,
    OrdersRepositoriesMixin,
    PaymentsRepositoriesMixin,
    ComplaintsRepositoriesMixin,
    BalancingRepositoriesMixin,
    AbstractAsyncContextManager
):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

        self._repositories = None

    @property
    def consents(self) -> UserConsentRepository:
        return self._get_or_create(
            "consents",
            lambda: UserConsentRepository(
                self.session,
                UserConsentMapper,
                UserConsentTable,
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

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError(
                "UnitOfWork no tiene una sesión activa."
            )

        await self.session.commit()
    
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
