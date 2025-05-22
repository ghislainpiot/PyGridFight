"""Game enumerations for PyGridFight domain."""

from enum import Enum


class GameStatus(str, Enum):
    """Game status enumeration."""
    WAITING = "waiting"
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class PlayerStatus(str, Enum):
    """Player status enumeration."""
    ONLINE = "online"
    OFFLINE = "offline"
    IN_GAME = "in_game"


class ActionType(str, Enum):
    """Action type enumeration."""
    MOVE = "move"
    ATTACK = "attack"
    COLLECT = "collect"
    USE_ITEM = "use_item"
    END_TURN = "end_turn"


class ResourceType(str, Enum):
    """Resource type enumeration."""
    ENERGY = "energy"
    MATERIALS = "materials"
    WEAPONS = "weapons"
    HEALTH = "health"


class TerrainType(str, Enum):
    """Terrain type enumeration."""
    EMPTY = "empty"
    WALL = "wall"
    RESOURCE = "resource"
    SPAWN = "spawn"


class Direction(str, Enum):
    """Direction enumeration."""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    NORTHEAST = "northeast"
    NORTHWEST = "northwest"
    SOUTHEAST = "southeast"
    SOUTHWEST = "southwest"


class AvatarType(str, Enum):
    """Avatar type enumeration."""
    WARRIOR = "warrior"
    SCOUT = "scout"
    ENGINEER = "engineer"
    MEDIC = "medic"


class ItemType(str, Enum):
    """Item type enumeration."""
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    TOOL = "tool"


class CombatResult(str, Enum):
    """Combat result enumeration."""
    HIT = "hit"
    MISS = "miss"
    CRITICAL = "critical"
    BLOCKED = "blocked"