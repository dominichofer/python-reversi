import unittest
from reversi.game import *


class TestIntensity(unittest.TestCase):
    def test_str_without_confidence_level(self):
        original = Intensity(10)
        intensity = str(original)
        round_trip = Intensity.from_string(intensity)
        self.assertEqual(original, round_trip)

    def test_str_with_confidence_level(self):
        i = Intensity(10, 1.0)
        self.assertEqual(i, Intensity.from_string(str(i)))

    def test_lt(self):
        self.assertLess(Intensity(5), Intensity(10))
        self.assertLess(Intensity(10, 1.0), Intensity(10))

    def test_is_exact(self):
        self.assertTrue(Intensity(10).is_exact())
        self.assertFalse(Intensity(10, 1.0).is_exact())


if __name__ == "__main__":
    unittest.main(verbosity=2)
