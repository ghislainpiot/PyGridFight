import pytest

from pygridfight.core.enums import ResourceTypeEnum
from pygridfight.gameplay.resources import Resource

def test_resource_initialization():
    """Resource initializes with correct type and value."""
    r = Resource(resource_type=ResourceTypeEnum.CURRENCY, value=5)
    assert r.resource_type == ResourceTypeEnum.CURRENCY
    assert r.value == 5

def test_resource_immutable():
    """Resource is immutable (frozen dataclass)."""
    r = Resource(resource_type=ResourceTypeEnum.CURRENCY, value=5)
    with pytest.raises(Exception):
        r.value = 10
    with pytest.raises(Exception):
        r.resource_type = ResourceTypeEnum.POWER_UP_SPEED_BOOST

def test_resource_equality():
    """Resource equality is based on type and value."""
    r1 = Resource(resource_type=ResourceTypeEnum.CURRENCY, value=5)
    r2 = Resource(resource_type=ResourceTypeEnum.CURRENCY, value=5)
    r3 = Resource(resource_type=ResourceTypeEnum.POWER_UP_SPEED_BOOST, value=5)
    r4 = Resource(resource_type=ResourceTypeEnum.CURRENCY, value=10)
    assert r1 == r2
    assert r1 != r3
    assert r1 != r4