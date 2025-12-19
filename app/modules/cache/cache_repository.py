from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, List

class CacheRepository(ABC):
    @abstractmethod
    async def cache_verify_connection(self) -> bool:
        """
        Verifies that the cache service is reachable and operational.

        Returns:
            bool: 
                True if the connection is active; otherwise, False.
        """
        pass

    @abstractmethod
    async def cache_set(
        self, 
        key: str, 
        data: Dict[str, Any], 
        seconds: Optional[int] = None
    ) -> bool:
        """
        Stores a single dictionary value in the cache with an optional expiration time.

        Args:
            key (str): 
                The cache key where the data will be stored.
            data (Dict[str, Any]): 
                The dictionary to serialize and store.
            ttl (Optional[int], optional): 
                Time-to-live in seconds. If None, the key does not expire.

        Returns:
            bool: 
                True if the data was cached successfully; otherwise, False.
        """
        pass

    @abstractmethod
    async def cache_get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves and deserializes a dictionary from the cache using the provided key.

        Args:
            key (str): 
                The cache key to look up.

        Returns:
            Optional[Dict[str, Any]]: 
                The stored dictionary if found; otherwise, None.
        """
        pass

    @abstractmethod
    async def cache_delete(self, key: str) -> None:
        """
        Removes a key-value pair from the cache.

        Args:
            key (str): 
                The cache key to delete.
        """
        pass