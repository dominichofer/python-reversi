import unittest
from reversi import *


class GameScoreTest(unittest.TestCase):

    def test_str(self):
        game = Game(Position.start(), [Field.E6, Field.F6])
        gs = GameScore(game, [+1, -1, +1])
        self.assertEqual(gs, GameScore.from_string(str(gs)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
