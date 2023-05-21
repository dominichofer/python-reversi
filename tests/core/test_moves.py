import unittest
from reversi import Moves, Field


class MovesTest(unittest.TestCase):

    def test_str(self):
        moves = str(Moves(0x8000000000000001))
        self.assertTrue('A1' in moves)
        self.assertTrue('H8' in moves)

    def test_iter(self):
        moves = list(Moves(0x8000000000000001))
        self.assertTrue(Field.A1 in moves)
        self.assertTrue(Field.H8 in moves)

    def test_getitem(self):
        moves = Moves(0x8000000000000001)
        self.assertEqual(moves[0], Field.H8)
        self.assertEqual(moves[1], Field.A1)

    def test_len(self):
        self.assertEqual(len(Moves(0x0000000000000000)), 0)
        self.assertEqual(len(Moves(0x8000000000000001)), 2)
        self.assertEqual(len(Moves(0xFFFFFFFFFFFFFFFF)), 64)

    def test_contains(self):
        moves = Moves(0x8000000000000001)
        self.assertTrue(Field.A1 in moves)
        self.assertTrue(Field.H8 in moves)

    def test_bool(self):
        self.assertFalse(Moves(0x0000000000000000))
        self.assertTrue(Moves(0x8000000000000001))


if __name__ == '__main__':
    unittest.main(verbosity=2)
