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
        start = time.perf_counter()
        value = perft(depth)
        stop = time.perf_counter()
        t = stop - start
        print(f"perft({depth}) = {value} ({t:.1f} s)")
        self.assertEqual(value, reference)


if __name__ == "__main__":
    unittest.main(verbosity=0)
