from typing import List
from uuid import UUID
from .avatar import Avatar

class Player:
    """
    Represents a player in the game.

    Attributes:
        player_id (UUID): Unique identifier for the player.
        display_name (str): The player's display name.
        avatars (List[Avatar]): List of the player's avatars.
        currency (int): The player's in-game currency.
    """

    def __init__(self, player_id: UUID, display_name: str, initial_currency: int = 0) -> None:
        """
        Initialize a Player.

        Args:
            player_id (UUID): Unique identifier for the player.
            display_name (str): The player's display name.
            initial_currency (int, optional): Starting currency. Defaults to 0.
        """
        self.player_id: UUID = player_id
        self.display_name: str = display_name
        self.avatars: List[Avatar] = []
        self.currency: int = initial_currency

    def add_avatar(self, avatar: Avatar) -> None:
        """
        Add an avatar to the player's avatar list.

        Args:
            avatar (Avatar): The avatar to add.
        """
        self.avatars.append(avatar)

    def remove_avatar(self, avatar_id_to_remove: UUID) -> None:
        """
        Remove an avatar from the player's avatar list by avatar_id.

        Args:
            avatar_id_to_remove (UUID): The ID of the avatar to remove.
        """
        self.avatars = [a for a in self.avatars if getattr(a, "avatar_id", None) != avatar_id_to_remove]

    def update_currency(self, amount: int) -> None:
        """
        Update the player's currency by a given amount. Currency cannot go below zero.

        Args:
            amount (int): The amount to add (positive) or subtract (negative).
        """
        self.currency += amount
        if self.currency < 0:
            self.currency = 0