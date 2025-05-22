from pygridfight.domain.models.avatar import Avatar
from pygridfight.domain.models.grid import Position
from pygridfight.domain.models.player import Player


def test_player_creation_and_score_updates():
    player = Player(id="p1", display_name="Alice")
    assert player.id == "p1"
    assert player.display_name == "Alice"
    assert player.score == 0
    assert player.avatar_ids == []

    player.increment_score(5)
    assert player.score == 5

    player.increment_score()
    assert player.score == 6

    player.reset_score()
    assert player.score == 0


def test_player_avatar_management():
    player = Player(id="p2", display_name="Bob")
    player.add_avatar("a1")
    assert "a1" in player.avatar_ids

    player.add_avatar("a2")
    assert set(player.avatar_ids) == {"a1", "a2"}

    player.remove_avatar("a1")
    assert "a1" not in player.avatar_ids
    assert "a2" in player.avatar_ids

    # Removing non-existent avatar should not raise
    player.remove_avatar("not_there")
    assert "a2" in player.avatar_ids


def test_avatar_creation_and_position_update():
    pos1 = Position(x=1, y=2)
    avatar = Avatar(id="a1", owner_id="p1", position=pos1)
    assert avatar.id == "a1"
    assert avatar.owner_id == "p1"
    assert avatar.position == pos1
    assert avatar.health == 1
    assert avatar.active is True

    pos2 = Position(x=3, y=4)
    avatar.set_position(pos2)
    assert avatar.position == pos2


def test_avatar_ownership_validation():
    player = Player(id="p3", display_name="Carol")
    avatar = Avatar(id="a2", owner_id=player.id, position=Position(x=0, y=0))
    assert avatar.owner_id == player.id

    # Ownership mismatch
    other_player = Player(id="p4", display_name="Dave")
    assert avatar.owner_id != other_player.id


def test_avatar_health_and_active_status():
    avatar = Avatar(id="a3", owner_id="p5", position=Position(x=0, y=0), health=2)
    assert avatar.is_alive() is True

    avatar.take_damage(1)
    assert avatar.health == 1
    assert avatar.is_alive() is True

    avatar.take_damage(1)
    assert avatar.health == 0
    assert avatar.is_alive() is False
    assert avatar.active is False

    # Healing after death should not revive (per current logic)
    avatar.heal(2)
    assert avatar.health == 0  # health does not increase after death
    assert avatar.active is False  # still not active

    # New avatar, test healing while alive
    avatar2 = Avatar(id="a4", owner_id="p6", position=Position(x=1, y=1), health=1)
    avatar2.heal(3)
    assert avatar2.health == 4
    assert avatar2.is_alive() is True
