from typing import Protocol, Callable, Any, Coroutine, Tuple, List
from fastapi.concurrency import run_in_threadpool
from app.core.app_exception import serialize_exception
import asyncio

class AsyncProtocol(Protocol):
    async def run_blocking(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        ...

    async def run_in_gather(self, *tasks, return_exceptions: bool = False) -> Tuple[List, List]:
        ...
    
    async def run_in_semaphore(self, semaphore: asyncio.Semaphore, func: Callable[..., Any], *args, **kwargs) -> Any:
        ...
        
    def create_semaphore(self, concurrency: int) -> asyncio.Semaphore:
        ...

class AsyncService(AsyncProtocol):
    async def run_blocking(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        return await run_in_threadpool(func, *args, **kwargs)
    
    async def run_in_gather(self, *tasks: Coroutine[Any, Any, Any], return_exceptions: bool = False) -> Tuple[List, List]:
        results = await asyncio.gather(*tasks, return_exceptions=return_exceptions)

        errors = []
        success = []

        for r in results:
            if isinstance(r, Exception):
                errors.append(serialize_exception(r))
            else:
                success.append(r)

        return success, errors
    
    async def run_in_semaphore(self, semaphore: asyncio.Semaphore, func: Callable[..., Any], *args, **kwargs) -> Any:
        async with semaphore:
            return await self.run_blocking(func, *args, **kwargs)
        
    def create_semaphore(self, concurrency: int) -> asyncio.Semaphore:
        return asyncio.Semaphore(concurrency)

    
def get_async_service() -> AsyncService:
    return AsyncService()
