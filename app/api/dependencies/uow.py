from app.infra.db.unit_of_work import UnitOfWork
from app.infra.db.config import async_session_factory
from typing import AsyncGenerator

async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(async_session_factory) as uow:
        yield uow