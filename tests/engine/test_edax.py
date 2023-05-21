import unittest
from reversi import Field, Line


class EdaxOutputTest(unittest.TestCase):

    def test_exact_depth(self):
        line = Line('  7|   24   -08        0:00.234      63133975  269803312 b3 C1 b1 A3 b2 H3 a5')

        self.assertEqual(line.index, 7)
        self.assertEqual(line.depth, 24)
        self.assertEqual(line.selectivity, None)
        self.assertEqual(line.confidence_level, float('inf'))
        self.assertEqual(line.score, -8)
        self.assertEqual(line.time, '0:00.234')
        self.assertEqual(line.nodes, 63133975)
        self.assertEqual(line.speed, 269803312)
        self.assertEqual(line.pv, [Field.B3, Field.C1, Field.B1, Field.A3, Field.B2, Field.H3, Field.A5])

    def test_depth_selectivity(self):
        line = Line('  8|25@98%  +03        0:00.094       9940593  105750989 G2 b8 B7 a2 A5 b2 G3')

        self.assertEqual(line.index, 8)
        self.assertEqual(line.depth, 25)
        self.assertEqual(line.selectivity, 98)
        self.assertEqual(line.confidence_level, 2.6)
        self.assertEqual(line.score, +3)
        self.assertEqual(line.time, '0:00.094')
        self.assertEqual(line.nodes, 9940593)
        self.assertEqual(line.speed, 105750989)
        self.assertEqual(line.pv, [Field.G2, Field.B8, Field.B7, Field.A2, Field.A5, Field.B2, Field.G3])

    def test_no_speed(self):
        line = Line('  1|   14   +18        0:00.000         95959            g8 H7 a8 A6 a4 A7 b6')

        self.assertEqual(line.index, 1)
        self.assertEqual(line.depth, 14)
        self.assertEqual(line.selectivity, None)
        self.assertEqual(line.confidence_level, float('inf'))
        self.assertEqual(line.score, +18)
        self.assertEqual(line.time, '0:00.000')
        self.assertEqual(line.nodes, 95959)
        self.assertEqual(line.speed, None)
        self.assertEqual(line.pv, [Field.G8, Field.H7, Field.A8, Field.A6, Field.A4, Field.A7, Field.B6])

    def test_pass(self):
        line = Line('  7|   24   -08        0:00.234      63133975  269803312 ps')

        self.assertEqual(line.index, 7)
        self.assertEqual(line.depth, 24)
        self.assertEqual(line.selectivity, None)
        self.assertEqual(line.confidence_level, float('inf'))
        self.assertEqual(line.score, -8)
        self.assertEqual(line.time, '0:00.234')
        self.assertEqual(line.nodes, 63133975)
        self.assertEqual(line.speed, 269803312)
        self.assertEqual(line.pv, [Field.PS])


if __name__ == '__main__':
    unittest.main(verbosity=2)
