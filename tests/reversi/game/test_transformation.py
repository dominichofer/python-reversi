import unittest
from reversi.game import *

pos1 = Position(0, 0)
pos2 = Position(0, 1)

scored_pos1 = ScoredPosition(pos1, +1)
scored_pos2 = ScoredPosition(pos2, -1)

game1 = Game(pos1, [Field.C4])
game2 = Game(pos2, [Field.A4, Field.B3])

scored_game1 = ScoredGame(game1, [+1, -1])
scored_game2 = ScoredGame(game2, [+1, -1, +2])


class TransformationTests(unittest.TestCase):
    def test_positions_of_game(self):
        self.assertEqual(len(list(positions(game1))), 2)

    def test_positions_of_scored_game(self):
        self.assertEqual(len(list(positions(scored_game1))), 2)

    def test_positions_of_game_range(self):
        games = [game1, game2]
        self.assertEqual(len(list(positions(games))), 5)

    def test_positions_of_scored_game_range(self):
        scored_games = [scored_game1, scored_game2]
        self.assertEqual(len(list(positions(scored_games))), 5)

    def test_positions_of_scored_position_range(self):
        scored_pos = [scored_pos1, scored_pos2]
        self.assertEqual(len(list(positions(scored_pos))), 2)

    def test_scores_of_scored_game(self):
        self.assertEqual(list(scores(scored_game1)), scored_game1.scores)

    def test_scores_of_scored_position_range(self):
        scored_pos = [scored_pos1, scored_pos2]
        reference = [scored_pos1.score, scored_pos2.score]
        self.assertEqual(list(scores(scored_pos)), reference)

    def test_scored_positions_of_scored_game_range(self):
        scored_games = [scored_game1, scored_game2]
        self.assertEqual(len(list(scored_positions(scored_games))), 5)

    def test_scored_positions_of_position_score_range(self):
        positions = [pos1, pos2]
        scores = [+1, -1]
        result = scored_positions(positions, scores)
        reference = [scored_pos1, scored_pos2]
        self.assertEqual(list(result), reference)
