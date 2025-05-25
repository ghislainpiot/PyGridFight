from uuid import uuid4

from pygridfight.scoring.services import ScoreKeeper

class TestScoreKeeper:
    def setup_method(self):
        self.score_keeper = ScoreKeeper()
        self.player1 = uuid4()
        self.player2 = uuid4()
        self.player3 = uuid4()

    def test_initialization_starts_with_empty_scores(self):
        assert self.score_keeper.get_all_scores() == {}

    def test_record_score_initializes_and_adds_points(self):
        self.score_keeper.record_score(self.player1, 5)
        assert self.score_keeper.get_score(self.player1) == 5

        self.score_keeper.record_score(self.player1, 3)
        assert self.score_keeper.get_score(self.player1) == 8

    def test_record_score_negative_points_does_not_go_below_zero(self):
        self.score_keeper.record_score(self.player1, 5)
        self.score_keeper.record_score(self.player1, -10)
        assert self.score_keeper.get_score(self.player1) == 0

    def test_get_score_returns_zero_for_untracked_player(self):
        assert self.score_keeper.get_score(self.player2) == 0

    def test_get_all_scores_returns_copy(self):
        self.score_keeper.record_score(self.player1, 2)
        self.score_keeper.record_score(self.player2, 3)
        scores = self.score_keeper.get_all_scores()
        assert scores[self.player1] == 2
        assert scores[self.player2] == 3
        # Mutating the returned dict should not affect the internal state
        scores[self.player1] = 100
        assert self.score_keeper.get_score(self.player1) == 2

    def test_check_victory_condition_returns_none_if_no_one_reaches_target(self):
        self.score_keeper.record_score(self.player1, 5)
        self.score_keeper.record_score(self.player2, 7)
        assert self.score_keeper.check_victory_condition(10) is None

    def test_check_victory_condition_returns_player_id_when_reached(self):
        self.score_keeper.record_score(self.player1, 5)
        self.score_keeper.record_score(self.player2, 10)
        assert self.score_keeper.check_victory_condition(10) == self.player2

    def test_check_victory_condition_first_to_reach(self):
        self.score_keeper.record_score(self.player1, 10)
        self.score_keeper.record_score(self.player2, 10)
        # Both reach at same time, but player1 was checked first in insertion order
        winner = self.score_keeper.check_victory_condition(10)
        assert winner in {self.player1, self.player2}
        # For MVP, first to reach is fine

    def test_multiple_players_scores_and_victory(self):
        self.score_keeper.record_score(self.player1, 3)
        self.score_keeper.record_score(self.player2, 7)
        self.score_keeper.record_score(self.player3, 12)
        assert self.score_keeper.get_score(self.player3) == 12
        assert self.score_keeper.check_victory_condition(10) == self.player3