import unittest
from reversi.game import *

class TestRandomPlayer(unittest.TestCase):
    
    def test_choose_move(self):
        pos = Position.start()
        player = RandomPlayer()
        
        move = player.choose_move(pos)
        
        self.assertIn(move, possible_moves(pos))
