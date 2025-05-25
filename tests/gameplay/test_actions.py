import uuid
import pytest
from pygridfight.gameplay.actions import MoveAction, CollectAction
from pygridfight.core.models import Coordinates

def test_move_action_instantiation():
    avatar_id = uuid.uuid4()
    coords = Coordinates(x=2, y=3)
    action = MoveAction(avatar_id=avatar_id, target_coordinates=coords)
    assert action.avatar_id == avatar_id
    assert action.target_coordinates == coords

def test_collect_action_instantiation():
    avatar_id = uuid.uuid4()
    coords = Coordinates(x=1, y=1)
    action = CollectAction(avatar_id=avatar_id, target_coordinates=coords)
    assert action.avatar_id == avatar_id
    assert action.target_coordinates == coords