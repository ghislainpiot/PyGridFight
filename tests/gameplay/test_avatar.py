import uuid
import pytest

from pygridfight.gameplay.avatar import Avatar
from pygridfight.core.models import Coordinates

def test_avatar_initialization():
    avatar_id = uuid.uuid4()
    player_id = uuid.uuid4()
    initial_position = Coordinates(x=2, y=3)
    avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=initial_position)

    assert avatar.avatar_id == avatar_id
    assert avatar.player_id == player_id
    assert avatar.position == initial_position
    assert isinstance(avatar.active_powerups, list)
    assert avatar.active_powerups == []

def test_avatar_move_updates_position():
    avatar_id = uuid.uuid4()
    player_id = uuid.uuid4()
    initial_position = Coordinates(x=1, y=1)
    avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=initial_position)

    new_position = Coordinates(x=4, y=5)
    avatar.move(new_position)

    assert avatar.position == new_position

def test_avatar_identity_is_constant():
    avatar_id = uuid.uuid4()
    player_id = uuid.uuid4()
    initial_position = Coordinates(x=0, y=0)
    avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=initial_position)

    new_position = Coordinates(x=9, y=9)
    avatar.move(new_position)

    assert avatar.avatar_id == avatar_id
    assert avatar.player_id == player_id