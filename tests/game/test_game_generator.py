import unittest
from typing import Iterable
from reversi.board import Field, Position
from reversi.game import *


class MockPlayer(Player):
    def __init__(self, pos: Position, moves: list[Field]):
        self.moves = {}
        for move in moves:
            self.moves[pos] = move
            pos = play(pos, move)

    def choose_move(self, pos: Position) -> Field:
        return self.moves.get(pos, Field.PS)

    def choose_moves(self, pos: Iterable[Position]) -> list[Field]:
        return [self.choose_move(p) for p in pos]


class TestGameGenerator(unittest.TestCase):
    def test_played_game(self):
        pos = Position.start()
        moves = [Field.D3, Field.C3]
        player = MockPlayer(pos, moves)

        game = played_game(player, player, pos)

        self.assertEqual(game, Game(pos, moves))

    def test_played_games(self):
        pos = Position.start()
        moves = [Field.D3, Field.C3]
        player = MockPlayer(pos, moves)
        starts = [pos] * 3

        games = played_games(player, player, starts)

        reference = [Game(pos, moves)] * 3
        self.assertEqual(games, reference)


if __name__ == "__main__":
    unittest.main(verbosity=2)
