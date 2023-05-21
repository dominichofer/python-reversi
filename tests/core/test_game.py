import unittest
from reversi import Position, Field, Game, is_game


class GameTest(unittest.TestCase):

    def test_move_string(self):
        game = Game(Position.start(), [Field.E6, Field.F6])
        self.assertEqual(game.moves_string(), 'E6 F6')

    def test_str(self):
        game = Game(Position.start(), [Field.E6, Field.F6])
        self.assertEqual(game, Game.from_string(str(game)))

    def test_play(self):
        game = Game()
        game.play(Field.E6)
        game.play(Field.F6)
        self.assertEqual(game, Game(Position.start(), [Field.E6, Field.F6]))

    def test_positions(self):
        game = Game()
        pos1 = game.current_position
        game.play(Field.E6)
        pos2 = game.current_position
        game.play(Field.F6)
        pos3 = game.current_position

        self.assertEqual([p for p in game.positions()], [pos1, pos2, pos3])
        

class IsGame(unittest.TestCase):
    def test_zero_ply(self):
        self.assertTrue(is_game('---------------------------OOO-----OOO-----OXO------X----------- X'))

    def test_one_ply(self):
        self.assertTrue(is_game('---------------------------OOO-----OOO-----OXO------X----------- X G6'))

    def test_two_ply(self):
        self.assertTrue(is_game('---------------------------OOO-----OOO-----OXO------X----------- X G6 D7'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
