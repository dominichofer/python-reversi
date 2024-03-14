import unittest
from reversi.search import (
    ClosedInterval,
    Field,
    Position,
    possible_moves,
    Result,
    Intensity,
    HashTable,
    sorted_by_mobility,
    sorted_by_mobility_and_tt,
)


class MoveSorterTest(unittest.TestCase):
    def test_sorted_by_mobility(self):
        pos = Position(0x0000100810000000, 0x0000201008000000)
        moves = sorted_by_mobility(pos, possible_moves(pos))
        self.assertEqual(moves[0], Field.C4)  # Lowest opponent mobility
        self.assertEqual(moves[-1], Field.B3)  # Highest opponent mobility

    def test_sorted_by_mobility_and_tt(self):
        pos = Position(0x0000100810000000, 0x0000201008000000)
        result = Result(ClosedInterval(-1, +1), Intensity(3, 1.0), Field.E6)
        tt = HashTable(1)
        tt.update(pos, result)  # mark E6 as best move

        moves = sorted_by_mobility_and_tt(tt)(pos, possible_moves(pos))

        self.assertEqual(moves[0], Field.E6)  # Best move
        self.assertEqual(moves[1], Field.C4)  # Lowest opponent mobility
        self.assertEqual(moves[-1], Field.B3)  # Highest opponent mobility
