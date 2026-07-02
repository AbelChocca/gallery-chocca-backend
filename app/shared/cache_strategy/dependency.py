from app.core.settings.pydantic_settings import get_settings, Settings
from app.shared.cache_strategy.cache_strategy_service import CacheStrategyService
from fastapi import Depends

def get_cache_strategy_service(
    settings: Settings = Depends(get_settings)
) -> CacheStrategyService:
    return CacheStrategyService(
        settings=settings
    )