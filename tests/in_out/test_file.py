import unittest
from pathlib import Path
from reversi.board import *
from reversi.game import *
from reversi.in_out import write_file, read_file


class GameFileTest(unittest.TestCase):

    @staticmethod
    def write_and_read(items):
        temp_file = Path('temp_file')
        try:
            write_file(temp_file, items)
            return read_file(temp_file)
        finally:
            temp_file.unlink()


    def test_pos_file(self):
        reference = [
            Position(1, 2),
            Position(4, 8),
        ]
        self.assertEqual(self.write_and_read(reference), reference)

    def test_pos_score_file(self):
        reference = [
            ScoredPosition(Position(1, 2), +3),
            ScoredPosition(Position(4, 8), -3),
        ]
        self.assertEqual(self.write_and_read(reference), reference)

    def test_game_file(self):
        reference = [
            Game(Position(1, 2), [Field.A1, Field.B1]),
            Game(Position(4, 8), [Field.A2, Field.B2]),
        ]
        self.assertEqual(self.write_and_read(reference), reference)

    def test_scored_game_file(self):
        reference = [
            ScoredGame(Game(Position(1, 2), [Field.A1, Field.B1]), [+1, +2, +3]),
            ScoredGame(Game(Position(4, 8), [Field.A2, Field.B2]), [-1, -2, -3]),
        ]
        self.assertEqual(self.write_and_read(reference), reference)
