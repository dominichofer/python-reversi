import unittest
from pathlib import Path
from parameterized import parameterized
from reversi import (
    PrincipalVariation,
    ScoredPosition,
    OpenInterval,
    min_score,
    max_score,
    read_file,
    HashTable,
)

endgame = read_file(Path(__file__).parent.parent.parent / "data" / "endgame.pos")


class PrincipalVariationTest(unittest.TestCase):
    @parameterized.expand(endgame)
    def test_endgame(self, scored_pos: ScoredPosition):
        result = PrincipalVariation().eval(scored_pos.pos)
        self.assertTrue(result.is_exact())
        self.assertEqual(result.window.lower, scored_pos.score)

    @parameterized.expand(endgame)
    def test_endgame_fail_low(self, scored_pos: ScoredPosition):
        window = OpenInterval(scored_pos.score, max_score)
        result = PrincipalVariation().eval(scored_pos.pos, window)
        self.assertLessEqual(result.window.upper, scored_pos.score)

    @parameterized.expand(endgame)
    def test_endgame_fail_high(self, scored_pos: ScoredPosition):
        window = OpenInterval(min_score, scored_pos.score)
        result = PrincipalVariation().eval(scored_pos.pos, window)
        self.assertGreaterEqual(result.window.lower, scored_pos.score)

    @parameterized.expand(endgame)
    def test_endgame_with_tt(self, scored_pos: ScoredPosition):
        tt = HashTable(1_000_000)
        result = PrincipalVariation(transposition_table=tt).eval(scored_pos.pos)
        self.assertTrue(result.is_exact())
        self.assertEqual(result.window.lower, scored_pos.score)    


if __name__ == "__main__":
    unittest.main(verbosity=2)
