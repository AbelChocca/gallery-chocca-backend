from redis.asyncio import Redis
from redis import RedisError, ConnectionError
from typing import Optional, Dict, Any, List, Union
from json import dumps, loads
from asyncio import sleep

from app.core.log.protocole import LoggerProtocol
from app.domain.cache.protocole import CacheProtocol
from app.infra.cache.exceptions import InternalCacheException

class RedisService(CacheProtocol):
    def __init__(
            self,
            cache_client: Redis,
            logger: LoggerProtocol
            ):
        self.client = cache_client
        self.logger = logger

    async def cache_verify_connection(self) -> bool:
        try:          
            pong = await self.client.ping()
            self.logger.info('✅ Conexión activa del cliente Redis verificada.')
            return pong is True
        except ConnectionError as e:
            self.logger.error(f'Error al hacer PING al cliente REDIS: {str(e)}')
            return False


    async def cache_set(
            self, key: str, 
            data: Union[Dict[str, Any], List[Dict[str, Any]]], 
            seconds: Optional[int] = None
        ) -> Optional[bool]:
        if not key:
            self.logger.warning(f"The input key: {key} is empty.")
            return False
        if not data:
           self.logger.warning('⚠️ The object data is empty.')
           return False
        try:
            json_data = dumps(data)
            await self.client.set(name=key, ex=seconds, value=json_data, nx=True)

            self.logger.info(f"Key: {key} was setted on cache successfully")
            return True
        except RedisError as e:
            self.logger.error(f'❌ Error al guardar la clave al cache: {str(e)}')
            raise InternalCacheException()
    
    async def cache_get(self, key: str) -> Optional[Any]:
        self.logger.info('⚙️ Verificando datos antes de obtener...')
    
        try:
            json_data = await self.client.get(key)
            if not json_data:
                self.logger.error('❌ La clave que intenta buscar no existe en el cache o ya venció.')
                return None
            result = loads(json_data)

            self.logger.info(f"Key: {key} value was getting successfully from redis service")
            return result
        except RedisError as e:
            self.logger.error(f'❌ Error del servidor al obtener el valor del cache: {str(e)}')
            raise InternalCacheException()

    async def cache_delete(self, key: str) -> None:
        try:
            delete = await self.client.delete(key)
            if delete:
                self.logger.info(f'✅ Cache key: {key} was deleted seccessfully.')
            else:
                self.logger.warning(f'⚠️ The key: {key} not exist in cache.')

            return True
        except RedisError as e:
            self.logger.error(f'❌ Error del servidor al eliminar clave del cache: {str(e)}')
            raise InternalCacheException()
        
    async def cache_set_lock(self, key: str, seconds: int = 5) -> bool:
        lock_key: str = f"lock:{key}"
        try:
            return await self.client.set(name=lock_key, value="1", ex=seconds, nx=True)
        except RedisError as e:
            self.logger.error(f"Redis service error to set the lock of key: {str(e)}")
            raise InternalCacheException()
        
    async def cache_retry_get(self, retries: int, key: str, seconds_delay: float) -> Optional[Any]:
        for attempt in range(retries):
            data = await self.client.get(key)

            if data is not None:
                return loads(data)

            if attempt < retries - 1:
                await sleep(seconds_delay)
        return None
