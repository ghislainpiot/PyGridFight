from typing import Dict, Optional
from uuid import UUID

class ScoreKeeper:
    """
    Service for tracking player scores and checking victory conditions.

    Attributes:
        _scores (Dict[UUID, int]): Internal mapping of player IDs to their scores.
    """

    def __init__(self) -> None:
        """
        Initializes the ScoreKeeper with an empty score dictionary.
        """
        self._scores: Dict[UUID, int] = {}

    def record_score(self, player_id: UUID, points: int) -> None:
        """
        Adds points to the specified player's score. Initializes the player's score if not present.
        Scores cannot go below zero.

        Args:
            player_id (UUID): The unique identifier of the player.
            points (int): The number of points to add (can be negative).
        """
        current = self._scores.get(player_id, 0)
        new_score = max(0, current + points)
        self._scores[player_id] = new_score

    def get_score(self, player_id: UUID) -> int:
        """
        Returns the current score for the specified player.

        Args:
            player_id (UUID): The unique identifier of the player.

        Returns:
            int: The player's score, or 0 if not tracked.
        """
        return self._scores.get(player_id, 0)

    def get_all_scores(self) -> Dict[UUID, int]:
        """
        Returns a copy of all tracked player scores.

        Returns:
            Dict[UUID, int]: Mapping of player IDs to their scores.
        """
        return self._scores.copy()

    def check_victory_condition(self, target_score: int) -> Optional[UUID]:
        """
        Checks if any player has reached or exceeded the target score.

        Args:
            target_score (int): The score required to win.

        Returns:
            Optional[UUID]: The player_id of the first player to reach or exceed the target score,
                            or None if no player has met the condition.
        """
        for player_id, score in self._scores.items():
            if score >= target_score:
                return player_id
        return None
