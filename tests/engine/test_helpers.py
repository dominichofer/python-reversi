import unittest
from reversi.engine.edax import split, flatten


class HelperTest(unittest.TestCase):
    def test_split(self):
        self.assertEqual(list(split([1, 2, 3, 4, 5], 1)), [[1, 2, 3, 4, 5]])
        self.assertEqual(list(split([1, 2, 3, 4, 5], 2)), [[1, 2, 3], [4, 5]])
        self.assertEqual(list(split([1, 2, 3, 4, 5], 3)), [[1, 2], [3, 4], [5]])
        self.assertEqual(list(split([1, 2, 3, 4, 5], 4)), [[1, 2], [3], [4], [5]])
        self.assertEqual(list(split([1, 2, 3, 4, 5], 5)), [[1], [2], [3], [4], [5]])
        self.assertEqual(list(split([1, 2, 3, 4, 5], 6)), [[1], [2], [3], [4], [5]])

    def test_flatten(self):
        self.assertEqual(flatten([[1, 2], [3, 4], [5]]), [1, 2, 3, 4, 5])
