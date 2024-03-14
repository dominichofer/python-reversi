import unittest
from parameterized import parameterized
from typing import Iterable
from reversi.board import Position, children


def count(i: Iterable):
    "Count the number of items in an iterable."
    return sum(1 for _ in i)


class ChildrenTest(unittest.TestCase):
    @parameterized.expand(
        [
            (1, 4),
            (2, 12),
            (3, 56),
            (4, 244),
            (5, 1_396),
            (6, 8_200),
            (7, 55_092),
        ]
    )
    def test_number_of_children(self, ply: int, num_children: int):
        pos = Position.start()
        self.assertEqual(count(children(pos, ply, True)), num_children)
        self.assertEqual(count(children(pos, ply, False)), num_children)

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
        self.assertEqual(count(children(pos, 1, True)), 1)
        self.assertEqual(count(children(pos, 1, False)), 4)

    def test_end_position(self):
        pos = Position()
        self.assertEqual(count(children(pos, 1, True)), 0)
        self.assertEqual(count(children(pos, 1, False)), 0)
