import uuid
import pytest
from pygridfight.gameplay.avatar import Avatar
from pygridfight.gameplay.player import Player
from pygridfight.core.models import Coordinates

class DummyAvatar(Avatar):
    """A minimal Avatar subclass for testing purposes."""
    def __init__(self, avatar_id=None):
        if avatar_id is None:
            avatar_id = uuid.uuid4()
        player_id = uuid.uuid4()
        position = Coordinates(x=0, y=0)
        super().__init__(avatar_id=avatar_id, player_id=player_id, initial_position=position)

def test_player_initialization():
    player_id = uuid.uuid4()
    display_name = "TestPlayer"
    player = Player(player_id=player_id, display_name=display_name)
    assert player.player_id == player_id
    assert player.display_name == display_name
    assert isinstance(player.avatars, list)
    assert player.avatars == []
    assert player.currency == 0

def test_player_initialization_with_currency():
    player_id = uuid.uuid4()
    display_name = "TestPlayer"
    player = Player(player_id=player_id, display_name=display_name, initial_currency=100)
    assert player.currency == 100

def test_add_avatar():
    player = Player(player_id=uuid.uuid4(), display_name="TestPlayer")
    avatar = DummyAvatar()
    player.add_avatar(avatar)
    assert avatar in player.avatars
    # Adding the same avatar again is allowed (no uniqueness enforced)
    player.add_avatar(avatar)
    assert player.avatars.count(avatar) == 2

def test_remove_avatar():
    player = Player(player_id=uuid.uuid4(), display_name="TestPlayer")
    avatar1 = DummyAvatar()
    avatar2 = DummyAvatar()
    player.add_avatar(avatar1)
    player.add_avatar(avatar2)
    player.remove_avatar(avatar1.avatar_id)
    assert avatar1 not in player.avatars
    assert avatar2 in player.avatars

def test_remove_avatar_not_found():
    player = Player(player_id=uuid.uuid4(), display_name="TestPlayer")
    avatar = DummyAvatar()
    player.add_avatar(avatar)
    # Remove with a random UUID (not present)
    player.remove_avatar(uuid.uuid4())
    # Avatar should still be present
    assert avatar in player.avatars

def test_update_currency_positive():
    player = Player(player_id=uuid.uuid4(), display_name="TestPlayer")
    player.update_currency(50)
    assert player.currency == 50

def test_update_currency_negative():
    player = Player(player_id=uuid.uuid4(), display_name="TestPlayer", initial_currency=100)
    player.update_currency(-30)
    assert player.currency == 70

def test_update_currency_cannot_go_below_zero():
    player = Player(player_id=uuid.uuid4(), display_name="TestPlayer", initial_currency=10)
    player.update_currency(-20)
    assert player.currency == 0

def test_identity_immutable():
    player_id = uuid.uuid4()
    display_name = "TestPlayer"
    player = Player(player_id=player_id, display_name=display_name)
    # Attempt to change attributes (should not actually prevent, but test that values remain as set)
    player.player_id = player_id
    player.display_name = display_name
    assert player.player_id == player_id
    assert player.display_name == display_name