import unittest
from reversi.in_out import Sizes


class SizesTest(unittest.TestCase):
    def test_total_size(self):
        self.assertEqual(Sizes.default(11).total_size, 11 * 8 + 7)
        self.assertEqual(Sizes.default(21).total_size, 21 * 8 + 7)

    def test_line_center(self):
        self.assertEqual(Sizes.default(11).line_center(0), 11)
        self.assertEqual(Sizes.default(11).line_center(1), 2 * 11 + 1)
        self.assertEqual(Sizes.default(11).line_center(2), 3 * 11 + 2)
        self.assertEqual(Sizes.default(21).line_center(0), 21)
        self.assertEqual(Sizes.default(21).line_center(1), 2 * 21 + 1)
        self.assertEqual(Sizes.default(21).line_center(2), 3 * 21 + 2)

    def test_field_center(self):
        self.assertEqual(Sizes.default(11).field_center(0), 11 // 2)
        self.assertEqual(Sizes.default(11).field_center(1), 11 + 11 // 2 + 1)
        self.assertEqual(Sizes.default(11).field_center(2), 2 * 11 + 11 // 2 + 2)
        self.assertEqual(Sizes.default(21).field_center(0), 21 // 2)
        self.assertEqual(Sizes.default(21).field_center(1), 21 + 21 // 2 + 1)
        self.assertEqual(Sizes.default(21).field_center(2), 2 * 21 + 21 // 2 + 2)
