
from pygridfight.core.enums import (
    GameStatusEnum,
    ResourceTypeEnum,
    PlayerActionEnum,
    PowerUpTypeEnum,
)

def test_game_status_enum_membership():
    assert GameStatusEnum.LOBBY.name == "LOBBY"
    assert GameStatusEnum.IN_PROGRESS.name == "IN_PROGRESS"
    assert GameStatusEnum.FINISHED.name == "FINISHED"
    assert GameStatusEnum.ABORTED.name == "ABORTED"
    for member in GameStatusEnum:
        assert isinstance(member, GameStatusEnum)

def test_resource_type_enum_membership():
    assert ResourceTypeEnum.CURRENCY.name == "CURRENCY"
    assert ResourceTypeEnum.POWER_UP_SPEED_BOOST.name == "POWER_UP_SPEED_BOOST"
    for member in ResourceTypeEnum:
        assert isinstance(member, ResourceTypeEnum)

def test_player_action_enum_membership():
    assert PlayerActionEnum.MOVE.name == "MOVE"
    assert PlayerActionEnum.COLLECT_RESOURCE.name == "COLLECT_RESOURCE"
    assert PlayerActionEnum.PURCHASE_AVATAR.name == "PURCHASE_AVATAR"
    assert PlayerActionEnum.USE_POWERUP.name == "USE_POWERUP"
    for member in PlayerActionEnum:
        assert isinstance(member, PlayerActionEnum)

def test_power_up_type_enum_membership():
    assert PowerUpTypeEnum.SPEED_BOOST.name == "SPEED_BOOST"
    for member in PowerUpTypeEnum:
        assert isinstance(member, PowerUpTypeEnum)

def test_enum_str_and_repr():
    # Check string representation and repr for one member of each enum
    assert str(GameStatusEnum.LOBBY) == "GameStatusEnum.LOBBY"
    assert repr(ResourceTypeEnum.CURRENCY).startswith("<ResourceTypeEnum.CURRENCY")
    assert str(PlayerActionEnum.MOVE) == "PlayerActionEnum.MOVE"
    assert "PowerUpTypeEnum.SPEED_BOOST" in repr(PowerUpTypeEnum.SPEED_BOOST)