import unittest
from reversi.game import *

class GameTest(unittest.TestCase):
    
    def test_str(self):
        game = Game(Position.start(), [Field.E6, Field.F6])
        self.assertEqual(game, Game.from_string(str(game)))

    def test_positions(self):
        pos = [Position.start()]
        game = Game()
        for move in [Field.E6, Field.F6]:
            pos.append(play(pos[-1], move))
            game.play(move)

        self.assertEqual(list(game.positions()), pos)

    def test_play(self):
        moves = [Field.E6, Field.F6]
        game = Game()
        for move in moves:
            game.play(move)
        self.assertEqual(game, Game(Position.start(), moves))

if __name__ == '__main__':
    unittest.main(verbosity=2)
