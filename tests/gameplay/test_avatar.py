import uuid
import pytest
from unittest.mock import Mock

from pygridfight.gameplay.avatar import Avatar
from pygridfight.core.models import Coordinates
from pygridfight.gameplay.exceptions import InvalidMoveError
from pygridfight.gameplay.resources import Resource
from pygridfight.core.enums import ResourceTypeEnum

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

def test_avatar_move_updates_position_with_valid_grid():
    avatar_id = uuid.uuid4()
    player_id = uuid.uuid4()
    initial_position = Coordinates(x=1, y=1)
    avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=initial_position)

    new_position = Coordinates(x=4, y=5)
    grid = Mock()
    grid.is_valid_coordinates.return_value = True
    grid.get_cell.return_value = object()

    avatar.move(new_position, grid)

    assert avatar.position == new_position
    grid.is_valid_coordinates.assert_called_once_with(new_position)
    grid.get_cell.assert_called_once_with(new_position)

def test_avatar_move_raises_invalid_move_error_for_out_of_bounds():
    avatar_id = uuid.uuid4()
    player_id = uuid.uuid4()
    initial_position = Coordinates(x=0, y=0)
    avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=initial_position)

    new_position = Coordinates(x=99, y=99)
    grid = Mock()
    grid.is_valid_coordinates.return_value = False

    with pytest.raises(InvalidMoveError):
        avatar.move(new_position, grid)
    grid.is_valid_coordinates.assert_called_once_with(new_position)

def test_avatar_move_raises_invalid_move_error_for_missing_cell():
    avatar_id = uuid.uuid4()
    player_id = uuid.uuid4()
    initial_position = Coordinates(x=0, y=0)
    avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=initial_position)

    new_position = Coordinates(x=1, y=1)
    grid = Mock()
    grid.is_valid_coordinates.return_value = True
    grid.get_cell.return_value = None

    with pytest.raises(InvalidMoveError):
        avatar.move(new_position, grid)
    grid.is_valid_coordinates.assert_called_once_with(new_position)
    grid.get_cell.assert_called_once_with(new_position)

def test_avatar_collect_resource_success():
    avatar_id = uuid.uuid4()
    player_id = uuid.uuid4()
    position = Coordinates(x=2, y=2)
    avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=position)

    grid = Mock()
    player = Mock()
    resource = Resource(resource_type=ResourceTypeEnum.CURRENCY, value=10)
    grid.collect_resource_at.return_value = resource

    collected = avatar.collect(grid, player)
    grid.collect_resource_at.assert_called_once_with(position)
    player.update_currency.assert_called_once_with(10)
    assert collected == resource

def test_avatar_collect_no_resource():
    avatar_id = uuid.uuid4()
    player_id = uuid.uuid4()
    position = Coordinates(x=2, y=2)
    avatar = Avatar(avatar_id=avatar_id, player_id=player_id, initial_position=position)

    grid = Mock()
    player = Mock()
    grid.collect_resource_at.return_value = None

    collected = avatar.collect(grid, player)
    grid.collect_resource_at.assert_called_once_with(position)
    player.update_currency.assert_not_called()
    assert collected is None