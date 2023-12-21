import unittest
from reversi.board import *

class FieldTest(unittest.TestCase):

    def test_bit(self):
        self.assertEqual(bit(Field.A1), 0x8000000000000000)
        self.assertEqual(bit(Field.H8), 0x1)

if __name__ == '__main__':
    unittest.main(verbosity=2)