import unittest
import time
from reversi import *


def timed_perft(depth: int) -> None:
    start = time.perf_counter()
    value = perft(depth)
    end = time.perf_counter()
    t = end - start

    s = f'perft({depth}) = {value}'
    if t > 0.1:
        print(s + f' ({t:.1f} s)')
    else:
        print(s)
    return value


class PerftTest(unittest.TestCase):

    def test_perft_0(self):
        self.assertEqual(timed_perft(0), 1)

    def test_perft_1(self):
        self.assertEqual(timed_perft(1), 4)

    def test_perft_2(self):
        self.assertEqual(timed_perft(2), 12)

    def test_perft_3(self):
        self.assertEqual(timed_perft(3), 56)

    def test_perft_4(self):
        self.assertEqual(timed_perft(4), 244)

    def test_perft_5(self):
        self.assertEqual(timed_perft(5), 1_396)

    def test_perft_6(self):
        self.assertEqual(timed_perft(6), 8_200)

    def test_perft_7(self):
        self.assertEqual(timed_perft(7), 55_092)

    def test_perft_8(self):
        self.assertEqual(timed_perft(8), 390_216)


if __name__ == '__main__':
    unittest.main(verbosity=0)
