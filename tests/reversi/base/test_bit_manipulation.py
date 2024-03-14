import unittest
from numpy import uint64
from reversi.base.bit_manipulation import get_lsb, cleared_lsb, countr_zero


class BitManipulationTest(unittest.TestCase):
    def test_get_lsb(self):
        self.assertEqual(get_lsb(uint64(0)), 0)
        self.assertEqual(get_lsb(uint64(1)), 1)
        self.assertEqual(get_lsb(uint64(2)), 2)
        self.assertEqual(get_lsb(uint64(3)), 1)
        self.assertEqual(get_lsb(uint64(4)), 4)
        self.assertEqual(get_lsb(uint64(5)), 1)
        self.assertEqual(get_lsb(uint64(0xFFFFFFFFFFFFFFFF)), 1)

    def test_cleared_lsb(self):
        self.assertEqual(cleared_lsb(uint64(0)), 0)
        self.assertEqual(cleared_lsb(uint64(1)), 0)
        self.assertEqual(cleared_lsb(uint64(2)), 0)
        self.assertEqual(cleared_lsb(uint64(3)), 2)
        self.assertEqual(cleared_lsb(uint64(4)), 0)
        self.assertEqual(cleared_lsb(uint64(5)), 4)
        self.assertEqual(cleared_lsb(uint64(0xFFFFFFFFFFFFFFFF)), 0xFFFFFFFFFFFFFFFE)

    def test_countr_zero(self):
        self.assertEqual(countr_zero(uint64(0)), 64)
        self.assertEqual(countr_zero(uint64(1)), 0)
        self.assertEqual(countr_zero(uint64(2)), 1)
        self.assertEqual(countr_zero(uint64(3)), 0)
        self.assertEqual(countr_zero(uint64(4)), 2)
        self.assertEqual(countr_zero(uint64(5)), 0)
        self.assertEqual(countr_zero(uint64(0xFFFFFFFFFFFFFFFF)), 0)
