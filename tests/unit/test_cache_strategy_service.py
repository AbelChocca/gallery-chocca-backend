from unittest.mock import Mock
import pytest

from app.shared.services.cache_strategy.cache_strategy_service import CacheStrategyService

def test_break_operation_by_id():
    settings = Mock()
    cache_strategy = CacheStrategyService(settings)

    with pytest.raises(TypeError):
        broken_operation = cache_strategy.operation_by_id(222, "12") # must be an integer

    broken_operation = cache_strategy.operation_by_id(222, 12)
    broken_key = cache_strategy.generate_key(broken_operation)

    fresh_operation = cache_strategy.operation_by_id("broken_operation", 12)
    fresh_key = cache_strategy.generate_key(fresh_operation)

    assert broken_key != fresh_key
    assert broken_operation.name == "unknow_name"
    assert type(broken_operation.name) == str