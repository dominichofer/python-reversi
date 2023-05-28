import unittest
from reversi import *


class PositionTest(unittest.TestCase):

    def test_start(self):
        self.assertEqual(Position.start().empty_count(), 60)

    def test_from_string_X_to_play(self):
        pos = Position.from_string('O--------------------------------------------------------------X X')
        self.assertEqual(pos, Position(1, 1 << 63))

    def test_from_string_O_to_play(self):
        pos = Position.from_string('O--------------------------------------------------------------X O')
        self.assertEqual(pos, Position(1 << 63, 1))

    def test_bytes(self):
        pos = Position.start()
        self.assertEqual(Position.from_bytes(bytes(pos)), pos)
        
    def test_str(self):
        self.assertEqual(str(Position.start()), '---------------------------OX------XO--------------------------- X')
        
    def test_multi_line_string(self):
        self.assertEqual(
            str(Position.start().multi_line_string()),
            (
            '  A B C D E F G H  \n'
            '1 - - - - - - - - 1\n'
            '2 - - - - - - - - 2\n'
            '3 - - - + - - - - 3\n'
            '4 - - + O X - - - 4\n'
            '5 - - - X O + - - 5\n'
            '6 - - - - + - - - 6\n'
            '7 - - - - - - - - 7\n'
            '8 - - - - - - - - 8\n'
            '  A B C D E F G H  ')
            )

    def test_eq(self):
        self.assertTrue(Position() == Position())
        self.assertFalse(Position() == Position(0, 1))

    def test_lt(self):
        self.assertTrue(Position() < Position(0, 1))
        self.assertFalse(Position(0, 1) < Position())

    def test_hash(self):
        hash(Position())

    def test_empties(self):
        self.assertEqual(Position().empties(), 0xFFFFFFFFFFFFFFFF)
        self.assertEqual(Position.start().empties(), 0xFFFFFFE7E7FFFFFF)

    def test_empty_count(self):
        self.assertEqual(Position().empty_count(), 64)
        self.assertEqual(Position.start().empty_count(), 60)


class IsPositionTest(unittest.TestCase):

    def test_X_player(self):
        self.assertTrue(is_position('O--------------------------------------------------------------X X'))

    def test_O_player(self):
        self.assertTrue(is_position('O--------------------------------------------------------------X O'))

    def test_no_player(self):
        self.assertFalse(is_position('O--------------------------------------------------------------X'))

    def test_score(self):
        self.assertFalse(is_position('O--------------------------------------------------------------X X % +60'))
        
        
class FlippedTest(unittest.TestCase):
    def test_codiagonal(self):
        self.assertEqual(flipped_codiagonal(Position(0x8080808000000000, 0x4040404000000000)),
                        Position(0x000000000000000F, 0x0000000000000F00))

    def test_diagonal(self):
        self.assertEqual(flipped_diagonal(Position(0x8080808000000000, 0x4040404000000000)),
                        Position(0xF000000000000000, 0x00F0000000000000))

    def test_horizontal(self):
        self.assertEqual(flipped_horizontal(Position(0x8080808000000000, 0x4040404000000000)),
                        Position(0x0101010100000000, 0x0202020200000000))

    def test_vertical(self):
        self.assertEqual(flipped_vertical(Position(0x8080808000000000, 0x4040404000000000)),
                        Position(0x0000000080808080, 0x0000000040404040))

    def test_to_unique(self):
        pos1 = Position(0x8080808000000000, 0x4040404000000000)
        pos2 = flipped_vertical(pos1)

        self.assertEqual(
            flipped_to_unique(pos1), 
            flipped_to_unique(pos2))


class PlayTest(unittest.TestCase):

    def test_play(self):
        pos = play(Position.start(), Field(19))
        self.assertEqual(pos, Position(0x0000001000000000, 0x0000000818080000))

    def test_play_pass(self):
        start = Position.start()
        passed = play_pass(start)
        passed2 = play_pass(passed)
        self.assertNotEqual(start, passed)
        self.assertNotEqual(passed, passed2)
        self.assertEqual(start, passed2)

    def test_possible_moves(self):
        self.assertEqual(possible_moves(Position.start()), Moves(0x0000102004080000))


class GameOverTest(unittest.TestCase):

    def test_is_game_over(self):
        self.assertTrue(is_game_over(Position()))
        self.assertFalse(is_game_over(Position.start()))

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


class ChildrenTest(unittest.TestCase):

    def test_number_of_children_at_1_ply(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 1, False)), 4)

    def test_number_of_children_at_2_ply(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 2, False)), 12)

    def test_number_of_children_at_3_ply(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 3, False)), 56)

    def test_number_of_children_at_4_ply(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 4, False)), 244)

    def test_number_of_children_at_5_ply(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 5, False)), 1_396)

    def test_number_of_children_at_6_ply(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 6, False)), 8_200)

    def test_number_of_children_at_7_ply(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 7, False)), 55_092)

    def test_possible_games_at_ply_1(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 1, True)), 4)

    def test_possible_games_at_ply_2(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 2, True)), 12)

    def test_possible_games_at_ply_3(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 3, True)), 56)

    def test_possible_games_at_ply_4(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 4, True)), 244)

    def test_possible_games_at_ply_5(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 5, True)), 1_396)

    def test_possible_games_at_ply_6(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 6, True)), 8_200)

    def test_possible_games_at_ply_7(self):
        self.assertEqual(sum(1 for _ in children(Position.start(), 7, True)), 55_092)

    def test_zero_plies_is_self(self):
        pos = Position.start()

        c = [x for x in children(pos, 0, True)]
        self.assertEqual(len(c), 1)
        self.assertTrue(pos in c)

        c = [x for x in children(pos, 0, False)]
        self.assertEqual(len(c), 1)
        self.assertTrue(pos in c)

    def test_passable_position(self):
        pos = Position(0x1800, 0xFF)
        self.assertEqual(sum(1 for _ in children(pos, 1, True)), 1)
        self.assertEqual(sum(1 for _ in children(pos, 1, False)), 4)

    def test_end_position(self):
        pos = Position()
        self.assertEqual(sum(1 for _ in children(pos, 1, True)), 0)
        self.assertEqual(sum(1 for _ in children(pos, 1, False)), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
