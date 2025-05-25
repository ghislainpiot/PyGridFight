from enum import Enum


class GameStatusEnum(Enum):
    """
    Enum representing the status of a game session.

    Members:
        LOBBY: Game is in the lobby/waiting state.
        IN_PROGRESS: Game is currently active.
        FINISHED: Game has ended normally.
        ABORTED: Game was aborted or cancelled.
    """
    LOBBY = "LOBBY"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    ABORTED = "ABORTED"


class ResourceTypeEnum(Enum):
    """
    Enum representing the types of resources available in the game.

    Members:
        CURRENCY: Standard in-game currency.
        POWER_UP_SPEED_BOOST: Power-up resource for speed boost.
    """
    CURRENCY = "CURRENCY"
    POWER_UP_SPEED_BOOST = "POWER_UP_SPEED_BOOST"


class PlayerActionEnum(Enum):
    """
    Enum representing possible player actions.

    Members:
        MOVE: Move the player's avatar.
        COLLECT_RESOURCE: Collect a resource from the grid.
        PURCHASE_AVATAR: Purchase a new avatar.
        USE_POWERUP: Use a power-up (included for extensibility).
    """
    MOVE = "MOVE"
    COLLECT_RESOURCE = "COLLECT_RESOURCE"
    PURCHASE_AVATAR = "PURCHASE_AVATAR"
    USE_POWERUP = "USE_POWERUP"


class PowerUpTypeEnum(Enum):
    """
    Enum representing the types of power-ups available.

    Members:
        SPEED_BOOST: Power-up that increases movement speed.
    """
    SPEED_BOOST = "SPEED_BOOST"
