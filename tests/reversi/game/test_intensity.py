import unittest
from reversi.game import *


class TestIntensity(unittest.TestCase):
    def test_str_without_confidence_level(self):
        original = Intensity(10)
        intensity = str(original)
        round_trip = Intensity.from_string(intensity)
        self.assertEqual(original, round_trip)

    def test_str_with_confidence_level(self):
        i = Intensity(10, 2.6)
        self.assertEqual(i, Intensity.from_string(str(i)))

    def test_bytes_without_confidence_level(self):
        original = Intensity(10)
        intensity = bytes(original)
        round_trip = Intensity.from_bytes(intensity)
        self.assertEqual(original, round_trip)

    def test_bytes_with_confidence_level(self):
        i = Intensity(10, 2.6)
        self.assertEqual(i, Intensity.from_bytes(bytes(i)))

    def test_lt(self):
        self.assertLess(Intensity(5), Intensity(10))
        self.assertLess(Intensity(10, 2.6), Intensity(10))

    def test_is_exact(self):
        self.assertTrue(Intensity(10).is_exact())
        self.assertFalse(Intensity(10, 2.6).is_exact())
