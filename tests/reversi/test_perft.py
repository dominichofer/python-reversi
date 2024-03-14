import unittest
import time
from parameterized import parameterized
from reversi import perft


class PerftTest(unittest.TestCase):
    @parameterized.expand(
        [
            (0, 1),
            (1, 4),
            (2, 12),
            (3, 56),
            (4, 244),
            (5, 1_396),
            (6, 8_200),
            (7, 55_092),
            (8, 390_216),
        ]
    )
    def test_perft(self, depth: int, reference: int):
        value = perft(depth)
        self.assertEqual(value, reference)
