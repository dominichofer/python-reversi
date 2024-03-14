import unittest
from reversi.base import *
from reversi.board import *
from reversi.game import *
from reversi.search import *


class TestHashTable(unittest.TestCase):
    def test_retrieves_inserted_value(self):
        pos = Position.start()
        result = Result(ClosedInterval(-1, +1), Intensity(3, 1.0), Field.A4)

        ht = HashTable(5)
        ht.update(pos, result)

        self.assertEqual(ht.look_up(pos), result)

    def test_retrieves_updated_value(self):
        pos = Position.start()
        result1 = Result(ClosedInterval(-1, +1), Intensity(3, 1.0), Field.A4)
        result2 = Result(ClosedInterval(-2, +2), Intensity(4, 1.0), Field.B5)

        ht = HashTable(5)
        ht.update(pos, result1)
        ht.update(pos, result2)

        self.assertEqual(ht.look_up(pos), result2)

    def test_retrieves_none_if_not_found(self):
        ht = HashTable(5)

        result = ht.look_up(Position.start())

        self.assertEqual(result, None)

    def test_retrieves_none_if_not_found_after_clear(self):
        pos = Position.start()
        result = Result(ClosedInterval(-1, +1), Intensity(3, 1.0), Field.A4)

        ht = HashTable(5)
        ht.update(pos, result)
        ht.clear()
        result = ht.look_up(pos)

        self.assertEqual(result, None)
