import unittest
from reversi.game import *


class TestFilter(unittest.TestCase):
    def test_Position(self):
        pos = [Position(0, 0), Position(0, 1), Position(0, 3)]
        empty_count = 63

        result = list(empty_count_filtered(pos, empty_count))

        reference = [pos[1]]
        self.assertEqual(result, reference)

    def test_Position_range(self):
        pos = [Position(0, 0), Position(0, 1), Position(0, 3)]
        lower = 62
        upper = 63

        result = list(empty_count_range_filtered(pos, lower, upper))

        reference = [pos[1], pos[2]]
        self.assertEqual(result, reference)

    def test_ScoredPosition(self):
        pos_score = [
            ScoredPosition(Position(0, 0), +1),
            ScoredPosition(Position(0, 1), -1),
            ScoredPosition(Position(0, 3), +1),
        ]
        empty_count = 63

        result = list(empty_count_filtered(pos_score, empty_count))

        reference = [pos_score[1]]
        self.assertEqual(result, reference)

    def test_ScoredPosition_range(self):
        pos_score = [
            ScoredPosition(Position(0, 0), +1),
            ScoredPosition(Position(0, 1), -1),
            ScoredPosition(Position(0, 3), +1),
        ]
        lower = 62
        upper = 63

        result = list(empty_count_range_filtered(pos_score, lower, upper))

        reference = [pos_score[1], pos_score[2]]
        self.assertEqual(result, reference)
