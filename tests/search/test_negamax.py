import unittest
from parameterized import parameterized
from pathlib import Path
from reversi import *

endgame = read_file(Path(__file__).parent.parent.parent / 'data' / 'endgame.pos')

class NegaMaxTest(unittest.TestCase):
    
    @parameterized.expand(endgame)
    def test_endgame(self, scored_pos: ScoredPosition):
        score = NegaMax().eval(scored_pos.pos)
        self.assertEqual(score, scored_pos.score)


if __name__ == '__main__':
    unittest.main(verbosity=2)
