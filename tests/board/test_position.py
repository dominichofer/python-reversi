import unittest
from reversi.board import (
    Field,
    Position,
    single_line_string,
    multi_line_string,
    flipped_codiagonal,
    flipped_diagonal,
    flipped_horizontal,
    flipped_vertical,
    flipped_to_unique,
    end_score,
)


class TestPosition(unittest.TestCase):
    def test_start(self):
        self.assertEqual(Position.start().empty_count(), 60)

    def test_from_string_X_to_play(self):
        pos = Position.from_string(
            "O--------------------------------------------------------------X X"
        )
        self.assertEqual(pos, Position(1, 1 << 63))

    def test_from_string_O_to_play(self):
        pos = Position.from_string(
            "O--------------------------------------------------------------X O"
        )
        self.assertEqual(pos, Position(1 << 63, 1))

    def test_from_illegal_string(self):
        self.assertRaises(IndexError, Position.from_string, "-------- X")

    def test_str(self):
        self.assertEqual(
            str(Position.start()),
            "---------------------------OX------XO--------------------------- X",
        )

    def test_single_line_string(self):
        self.assertEqual(
            single_line_string(Position.start()),
            "---------------------------OX------XO--------------------------- X",
        )

        self.assertEqual(
            single_line_string(Position(0, 0xFFFFFFFFFFFFFFFF)),
            "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO X",
        )

    def test_multi_line_string(self):
        self.assertEqual(
            multi_line_string(Position.start()),
            "  A B C D E F G H  \n"
            "1 - - - - - - - - 1\n"
            "2 - - - - - - - - 2\n"
            "3 - - - - - - - - 3\n"
            "4 - - - O X - - - 4\n"
            "5 - - - X O - - - 5\n"
            "6 - - - - - - - - 6\n"
            "7 - - - - - - - - 7\n"
            "8 - - - - - - - - 8\n"
            "  A B C D E F G H  ",
        )

    def test_eq(self):
        self.assertTrue(Position() == Position())
        self.assertFalse(Position() == Position(0, 1))

    def test_lt(self):
        self.assertTrue(Position() < Position(0, 1))
        self.assertFalse(Position(0, 1) < Position())

    def test_hash(self):
        hash(Position())

    def test_player_at(self):
        pos = Position.start()
        self.assertFalse(pos.player_at(Field.D3))
        self.assertFalse(pos.player_at(Field.D4))
        self.assertTrue(pos.player_at(Field.D5))

    def test_opponent_at(self):
        pos = Position.start()
        self.assertFalse(pos.opponent_at(Field.D3))
        self.assertTrue(pos.opponent_at(Field.D4))
        self.assertFalse(pos.opponent_at(Field.D5))

    def test_discs(self):
        self.assertEqual(Position(1, 2).discs(), 3)

    def test_empties(self):
        self.assertEqual(Position().empties(), 0xFFFFFFFFFFFFFFFF)
        self.assertEqual(Position.start().empties(), 0xFFFFFFE7E7FFFFFF)

    def test_empty_count(self):
        self.assertEqual(Position().empty_count(), 64)
        self.assertEqual(Position.start().empty_count(), 60)


class FlippedTest(unittest.TestCase):
    def test_codiagonal(self):
        self.assertEqual(
            flipped_codiagonal(Position(0x8080808000000000, 0x4040404000000000)),
            Position(0x000000000000000F, 0x0000000000000F00),
        )

    def test_diagonal(self):
        self.assertEqual(
            flipped_diagonal(Position(0x8080808000000000, 0x4040404000000000)),
            Position(0xF000000000000000, 0x00F0000000000000),
        )

    def test_horizontal(self):
        self.assertEqual(
            flipped_horizontal(Position(0x8080808000000000, 0x4040404000000000)),
            Position(0x0101010100000000, 0x0202020200000000),
        )

    def test_vertical(self):
        self.assertEqual(
            flipped_vertical(Position(0x8080808000000000, 0x4040404000000000)),
            Position(0x0000000080808080, 0x0000000040404040),
        )

    def test_to_unique(self):
        pos = Position(0xFF80000000000000, 0x00000000000003FF)
        all_pos = [
            pos,
            flipped_codiagonal(pos),
            flipped_diagonal(pos),
            flipped_horizontal(pos),
            flipped_vertical(pos),
            flipped_codiagonal(flipped_diagonal(pos)),
            flipped_codiagonal(flipped_horizontal(pos)),
            flipped_codiagonal(flipped_vertical(pos)),
        ]
        ref = flipped_to_unique(pos)
        for p in all_pos:
            self.assertEqual(flipped_to_unique(p), ref)


class EndScoreTest(unittest.TestCase):
    def test_all_player(self):
        pos = Position(0xFFFFFFFFFFFFFFFF, 0)
        self.assertEqual(end_score(pos), +64)

    def test_all_opponent(self):
        pos = Position(0, 0xFFFFFFFFFFFFFFFF)
        self.assertEqual(end_score(pos), -64)

    def test_half_half(self):
        pos = Position(0xFF, 0xFF00)
        self.assertEqual(end_score(pos), 0)

    def test_more_than_half(self):
        pos = Position(0xFF, 0x1FF00)
        self.assertEqual(end_score(pos), -48)


if __name__ == "__main__":
    unittest.main(verbosity=2)
