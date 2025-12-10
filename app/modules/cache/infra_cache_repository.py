from redis.asyncio import Redis
from redis import RedisError, ConnectionError
from typing import Optional, List, Dict, Any
from json import dumps, loads

from app.core.log.repository_logger import LoggerRepository
from app.modules.cache.cache_repository import CacheRepository
from app.shared.exceptions.infra.infraestructure_exception import InternalCacheException

class InfraCacheRepository(CacheRepository):
    def __init__(
            self,
            cache_client: Redis,
            logger: LoggerRepository
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


    async def cache_setex(self, key: str, data: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        if not data:
           self.logger.warning('⚠️ El dato string de entrada esta vacio.')
           return False
        try:
            json_data = dumps(data)
            await self.client.setex(name=key, time=ttl, value=json_data)
            return True
        except RedisError as e:
            self.logger.error(f'❌ Error al guardar la clave al cache: {str(e)}')
            raise InternalCacheException()
    
    async def cache_get(self, key: str) -> Optional[Dict[str, Any]]:
        self.logger.info('⚙️ Verificando datos antes de obtener...')

        json_data = await self.client.get(key)
        if not json_data:
           self.logger.error('❌ La clave que intenta buscar no existe en el cache o ya venció.')
           return None
    
        try:
            result = loads(json_data)
            return result
        except RedisError as e:
            self.logger.error(f'❌ Error del servidor al obtener el valor del cache: {str(e)}')
            raise InternalCacheException()

    async def cache_delete(self, key: str) -> bool:
        if not(await self.client.get(key)):
            self.logger.error('❌ La clave a eliminar no existe en el cache.')
            return False
        
        try:
            await self.client.delete(key)
            self.logger.info('✅ Clave borrado del cache correctamente.')

            return True
        except RedisError as e:
            self.logger.error(f'❌ Error del servidor al eliminar clave del cache: {str(e)}')
            raise InternalCacheException
        
    async def cache_set_list(self, key: str, data: List[Dict[str, Any]], ttl: Optional[int] = None) -> bool:
        if not data:
            self.logger.error('❌ No se encontro ningun dato dentro de la lista de instancias.')
            return False
        
        try:
            json_data = dumps(data)

            await self.client.setex(name=key, value=json_data, time=ttl)
            self.logger.info('✅ Productos cacheados correctamente.')
            return True
        except RedisError as e:
            self.logger.error(f'❌ Hubo un error del servidor al cachear los datos: {str(e)}')
            raise InfraCacheRepository()

    async def cache_get_list(self, key: str) -> Optional[List[Dict[str, Any]]]:
        response = await self.client.get(key) # Obtenemos datos serializados
        if not response:
            self.logger.warning('⚠️ No existe o caduco el tiempo de espera del objeto en redis.')
            return None
        
        try:
            data = loads(response)

            return data
        except RedisError as e:
            self.logger.error('❌ Error del servidor Redis al obtener datos del cache: %s', str(e))
            raise InfraCacheRepository()
        