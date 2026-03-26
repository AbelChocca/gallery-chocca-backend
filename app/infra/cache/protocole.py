from typing import Dict, Any, List, Protocol, Callable, Awaitable

class CacheProtocol(Protocol):
    async def cache_verify_connection(self) -> bool:
        """
        Verifies that the cache service is reachable and operational.

        Returns:
            bool: 
                True if the connection is active; otherwise, False.
        """
        ...

    async def cache_set(
        self, 
        key: str, 
        data: Dict[str, Any] | List[Dict[str, Any]], 
        seconds: int | None = None
    ) -> bool:
        """
        Stores a single dictionary value in the cache with an optional expiration time.

        Args:
            key (str): 
                The cache key where the data will be stored.
            data (Union[List[Dict], Dict]): 
                The List of dictionary or dictionary to serialize and store.
            ttl (Optional[int], optional): 
                Time-to-live in seconds. If None, the key does not expire.

        Returns:
            bool: 
                True if the data was cached successfully; otherwise, False.
        """
        ...

    async def cache_get(self, key: str) -> Any | None:
        """
        Retrieves and deserializes a dictionary from the cache using the provided key.

        Args:
            key (str): 
                The cache key to look up.

        Returns:
            Optional[Dict[str, Any]]: 
                The stored dictionary if found; otherwise, None.
        """
        ...

    async def cache_delete(self, key: str) -> None:
        """
        Removes a key-value pair from the cache.

        Args:
            key (str): 
                The cache key to delete.
        """
        ...

    async def get_or_set_with_lock(
            self,
            key: str,
            ttl: int,
            callback: Callable[..., Awaitable[Any] | Any],
            kwargs: dict,
            lock_ttl: int = 5,
    ) -> Any:
        """
        Set a lock value for restauring the current key removed
        
        :param self: default
        :param key: current key for restart
        :type key: str
        :param seconds: duration of the lock's key in seconds
        :type seconds: int
        :return: True if the lock's key was setted Else if not
        :rtype: bool
        """
        ...

    async def cache_retry_get(self, key: str, retries: int, delay: float) -> Any | None:
        """
        Method to execute a loop in a range of retries count for obtain the key value
        
        :param self: defaul
        :param retries: max retries for obtain de key value
        :type retries: int
        :param key: the key of the value setted
        :type key: str
        :param seconds_delay: delay in seconds after retry obtain the value
        :type seconds_delay: float
        :return: None if the method wasn't return any value. Key value if it could be obtained
        :rtype: any | None
        """
        ...

    async def invalidate_family(self, key: str) -> None:
        ...