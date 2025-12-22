from abc import ABC, abstractmethod
from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.dto.product_dto import FilterSchemaDTO
from typing import List

class ProductRepository(ABC):
    @abstractmethod
    async def save(self, product: Product) -> Product:
        """
        Method to save the product instance entity to the database service
        
        :param self: default
        :param product: instance of the product entity
        :type product: Product
        :return: Product with his current id in database
        :rtype: Product
        """
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Product:
        """
        Method to get a product object from database by his id
        
        :param self: default
        :param id: id of the product
        :type id: int
        :return: Product from the database memory
        :rtype: Product
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        filter_dto: FilterSchemaDTO,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        """
        Method to get products from offset to limit with filter methods
        
        :param self: default
        :param filter_dto: filter data object
        :type filter_dto: FilterSchemaDTO
        :param offset: start integer of the range 
        :type offset: int
        :param limit: limit integer of the range 
        :type limit: int
        :return: the list of products from offset to limit with filtered values
        :rtype: List[Product]
        """
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
    async def search_related(self, query: str, offset: int, limit: int) -> List[Product]:
        """
        Search a short list of products related to the query param
        
        :param self: default
        :param query: text related to product's name
        :type query: str
        :param offset: start of pagination
        :type offset: int
        :param limit: limit of the page
        :type limit: int
        :return: The list of products related to query param
        :rtype: List[Product]
        """
        pass