import unittest
from reversi.game import *

class ScoredPositionTest(unittest.TestCase):
    
    def test_from_string_score(self):
        self.assertEqual(
            ScoredPosition.from_string('O--------------------------------------------------------------X O % +02'),
            ScoredPosition(Position(1 << 63, 1), +2)
           )
        
    def test_str(self):
        ps = ScoredPosition(Position.start(), -7)
        self.assertEqual(str(ps), '---------------------------OX------XO--------------------------- X % -07')

if __name__ == '__main__':
    unittest.main(verbosity=2)