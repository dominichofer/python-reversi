import unittest
from reversi.core.bit_manipulation import *

class BitManipulationTest(unittest.TestCase):

    def test_get_lsb(self):
        self.assertEqual(get_lsb(0), 0)
        self.assertEqual(get_lsb(1), 1)
        self.assertEqual(get_lsb(2), 2)
        self.assertEqual(get_lsb(3), 1)
        self.assertEqual(get_lsb(4), 4)
        self.assertEqual(get_lsb(5), 1)
        self.assertEqual(get_lsb(0xFFFFFFFFFFFFFFFF), 1)

    def test_cleared_lsb(self):
        self.assertEqual(cleared_lsb(0), 0)
        self.assertEqual(cleared_lsb(1), 0)
        self.assertEqual(cleared_lsb(2), 0)
        self.assertEqual(cleared_lsb(3), 2)
        self.assertEqual(cleared_lsb(4), 0)
        self.assertEqual(cleared_lsb(5), 4)
        self.assertEqual(cleared_lsb(0xFFFFFFFFFFFFFFFF), 0xFFFFFFFFFFFFFFFE)

    def test_countr_zero(self):
        self.assertEqual(countr_zero(0), 64)
        self.assertEqual(countr_zero(1), 0)
        self.assertEqual(countr_zero(2), 1)
        self.assertEqual(countr_zero(3), 0)
        self.assertEqual(countr_zero(4), 2)
        self.assertEqual(countr_zero(5), 0)
        self.assertEqual(countr_zero(0xFFFFFFFFFFFFFFFF), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
