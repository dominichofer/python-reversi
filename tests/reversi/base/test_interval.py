import unittest
from reversi.base import *

class OpenIntervalTest(unittest.TestCase):
    
    def test_equality(self):
        i1 = OpenInterval(1, 3)
        i2 = OpenInterval(1, 3)
        i3 = OpenInterval(2, 4)

        self.assertEqual(i1, i2)
        self.assertNotEqual(i1, i3)

    def test_negation_operator(self):
        i = OpenInterval(1, 3)
        self.assertEqual(-i, OpenInterval(-3, -1))

    def test_contains(self):
        i = OpenInterval(1, 3)

        self.assertFalse(1 in i)
        self.assertTrue(2 in i)
        self.assertFalse(3 in i)

    def test_compare(self):
        i = OpenInterval(1, 3)

        self.assertTrue(1 < i)
        self.assertFalse(2 < i)
        self.assertFalse(2 > i)
        self.assertTrue(3 > i)
        self.assertTrue(i > 1)
        self.assertFalse(i > 2)
        self.assertFalse(i < 2)
        self.assertTrue(i < 3)

        self.assertTrue(OpenInterval(-3, 1) < i)
        self.assertFalse(OpenInterval(-3, 2) < i)
        self.assertFalse(OpenInterval(2, 6) > i)
        self.assertTrue(OpenInterval(3, 6) > i)
        self.assertTrue(i > OpenInterval(-3, 1))
        self.assertFalse(i > OpenInterval(-3, 2))
        self.assertFalse(i < OpenInterval(2, 6))
        self.assertTrue(i < OpenInterval(3, 6))

        self.assertTrue(ClosedInterval(-3, 1) < i)
        self.assertFalse(ClosedInterval(-3, 2) < i)
        self.assertFalse(ClosedInterval(2, 6) > i)
        self.assertTrue(ClosedInterval(3, 6) > i)
        self.assertTrue(i > ClosedInterval(-3, 1))
        self.assertFalse(i > ClosedInterval(-3, 2))
        self.assertFalse(i < ClosedInterval(2, 6))
        self.assertTrue(i < ClosedInterval(3, 6))

class ClosedIntervalTest(unittest.TestCase):
    
    def test_equality(self):
        i1 = ClosedInterval(1, 3)
        i2 = ClosedInterval(1, 3)
        i3 = ClosedInterval(2, 4)

        self.assertEqual(i1, i2)
        self.assertNotEqual(i1, i3)

    def test_less_than_operator(self):
        i = ClosedInterval(1, 3)

        self.assertTrue(0 < i)
        self.assertFalse(1 < i)
        self.assertFalse(3 > i)
        self.assertTrue(4 > i)
        self.assertTrue(i > 0)
        self.assertFalse(i > 1)
        self.assertFalse(i < 3)
        self.assertTrue(i < 4)

        self.assertTrue(OpenInterval(-3, 1) < i)
        self.assertFalse(OpenInterval(-3, 2) < i)
        self.assertFalse(OpenInterval(2, 6) > i)
        self.assertTrue(OpenInterval(3, 6) > i)
        self.assertTrue(i > OpenInterval(-3, 1))
        self.assertFalse(i > OpenInterval(-3, 2))
        self.assertFalse(i < OpenInterval(2, 6))
        self.assertTrue(i < OpenInterval(3, 6))

        self.assertTrue(ClosedInterval(-3, 0) < i)
        self.assertFalse(ClosedInterval(-3, 1) < i)
        self.assertFalse(ClosedInterval(3, 6) > i)
        self.assertTrue(ClosedInterval(4, 6) > i)
        self.assertTrue(i > ClosedInterval(-3, 0))
        self.assertFalse(i > ClosedInterval(-3, 1))
        self.assertFalse(i < ClosedInterval(3, 6))
        self.assertTrue(i < ClosedInterval(4, 6))

    def test_contains(self):
        i = ClosedInterval(1, 3)

        self.assertFalse(0 in i)
        self.assertTrue(1 in i)
        self.assertTrue(2 in i)
        self.assertTrue(3 in i)
        self.assertFalse(4 in i)

    def test_overlaps(self):
        i = ClosedInterval(1, 3)

        self.assertFalse(i.overlaps(OpenInterval(-1, 1)))
        self.assertTrue(i.overlaps(OpenInterval(-1, 2)))
        self.assertTrue(i.overlaps(OpenInterval(2, 6)))
        self.assertFalse(i.overlaps(OpenInterval(3, 6)))
        

class IntersectionTest(unittest.TestCase):
    
    def test_open_open_is_open(self):
        i1 = OpenInterval(1, 3)
        i2 = OpenInterval(2, 4)

        self.assertEqual(intersection(i1, i2), OpenInterval(2, 3))
        
    def test_closed_closed_is_closed(self):
        i1 = ClosedInterval(1, 3)
        i2 = ClosedInterval(2, 4)

        self.assertEqual(intersection(i1, i2), ClosedInterval(2, 3))
        
    def test_mixed_type_raises(self):
        self.assertRaises(TypeError, intersection, OpenInterval(1, 3), ClosedInterval(2, 4))
        self.assertRaises(TypeError, intersection, ClosedInterval(1, 3), OpenInterval(2, 4))
