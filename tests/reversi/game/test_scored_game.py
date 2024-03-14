import unittest
from reversi.game import *

class ScoredGameTest(unittest.TestCase):

    def test_str(self):
        game = Game(Position.start(), [Field.E6, Field.F6])
        sg = ScoredGame(game, [+1, -1, +10])
        self.assertEqual(sg, ScoredGame.from_string(str(sg)))
