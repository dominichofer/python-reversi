import unittest
from reversi import CassandraLine, Intensity, Field


class CassandraOutputTest(unittest.TestCase):
    def test_no_selectivity(self):
        line = CassandraLine(
            "    1'000|14     | +00 |     |        0.020 |             11 |   1'250'000 | PS"
        )
        self.assertEqual(line.index, 1_000)
        self.assertEqual(line.intensity, Intensity(14))
        self.assertEqual(line.score, 0)
        self.assertEqual(line.time, "0.020")
        self.assertEqual(line.nodes, 11)
        self.assertEqual(line.speed, 1_250_000)
        self.assertEqual(line.pv, [Field.PS])

    def test_depth_selectivity(self):
        line = CassandraLine(
            "    1'000|14@1.1 | +00 |     |        0.020 |             11 |   1'250'000 | PS"
        )
        self.assertEqual(line.index, 1_000)
        self.assertEqual(line.intensity, Intensity(14, 1.1))
        self.assertEqual(line.score, 0)
        self.assertEqual(line.time, "0.020")
        self.assertEqual(line.nodes, 11)
        self.assertEqual(line.speed, 1_250_000)
        self.assertEqual(line.pv, [Field.PS])
