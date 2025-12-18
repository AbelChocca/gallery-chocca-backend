from abc import ABC, abstractmethod
from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.dto.product_dto import FilterSchemaDTO
from typing import List

class ProductRepository(ABC):
    @abstractmethod
    async def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Product:
        pass

    @abstractmethod
    async def get_all(
        self,
        filter_dto: FilterSchemaDTO,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        pass

    @abstractmethod
    async def count_filtered_products(
        self,
        filter_dto: FilterSchemaDTO
    ) -> int:
        pass

    @abstractmethod
    async def delete_by_id(self, id: int) -> None:
        pass

    @abstractmethod
    async def delete_variant_by_id(self, variant_id: int) -> None:
        pass

    @abstractmethod
    async def delete_image_by_id(self, cloudinary_id: str) -> None:
        pass