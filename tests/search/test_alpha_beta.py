import unittest
from parameterized import parameterized
from pathlib import Path
from reversi import *

endgame = read_file(Path(__file__).parent.parent.parent / "data" / "endgame.pos")


class AlphaBetaTest(unittest.TestCase):
    @parameterized.expand(endgame)
    def test_endgame(self, scored_pos: ScoredPosition):
        score = AlphaBeta().eval(scored_pos.pos)
        self.assertEqual(score, scored_pos.score)

    @parameterized.expand(endgame)
    def test_endgame_fail_low(self, scored_pos: ScoredPosition):
        window = OpenInterval(scored_pos.score, max_score)
        score = AlphaBeta().eval(scored_pos.pos, window)
        self.assertLessEqual(score, scored_pos.score)

    @parameterized.expand(endgame)
    def test_endgame_fail_high(self, scored_pos: ScoredPosition):
        window = OpenInterval(min_score, scored_pos.score)
        score = AlphaBeta().eval(scored_pos.pos, window)
        self.assertGreaterEqual(score, scored_pos.score)


# Integration test of AlphaBeta and move sorters.
class MoveSortedAlphaBetaTest(unittest.TestCase):
    @parameterized.expand(endgame)
    def test_endgame_with_mobility_sorting(self, scored_pos: ScoredPosition):
        score = AlphaBeta(sorted_by_mobility).eval(
            scored_pos.pos,
        )
        self.assertEqual(score, scored_pos.score)


if __name__ == "__main__":
    unittest.main(verbosity=2)
