import unittest
from numpy import uint64
from reversi.board.bitboard import *

class BitBoardTest(unittest.TestCase):

    def test_flipped_codiagonal(self):
        self.assertEqual(flipped_codiagonal(uint64(0xF)), 0x8080808000000000)

    def test_flipped_diagonal(self):
        self.assertEqual(flipped_diagonal(uint64(0xF)), 0x01010101)

    def test_flipped_horizontal(self):
        self.assertEqual(flipped_horizontal(uint64(0xF)), 0xF0)

    def test_flipped_vertical(self):
        self.assertEqual(flipped_vertical(uint64(0xF)), 0x0F00000000000000)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    