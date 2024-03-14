import unittest
from reversi.in_out import is_position, is_scored_position, is_game, is_scored_game

class IsPositionTest(unittest.TestCase):

    def test_X_to_play(self):
        self.assertTrue(is_position('O--------------------------------------------------------------X X'))

    def test_O_to_play(self):
        self.assertTrue(is_position('O--------------------------------------------------------------X O'))

    def test_no_player(self):
        self.assertFalse(is_position('O--------------------------------------------------------------X'))

    def test_with_score(self):
        self.assertFalse(is_position('O--------------------------------------------------------------X X % +60'))
        

class IsScoredPosition(unittest.TestCase):
    
    def test_X_to_play(self):
        self.assertTrue(is_scored_position('O--------------------------------------------------------------X X % +60'))

    def test_O_to_play(self):
        self.assertTrue(is_scored_position('O--------------------------------------------------------------X O % -60'))

    def test_no_player(self):
        self.assertFalse(is_scored_position('O--------------------------------------------------------------X % +60'))


class IsGameTest(unittest.TestCase):
    
    def test_zero_moves(self):
        self.assertTrue(is_game('---------------------------OOO-----OOO-----OXO------X----------- X'))

    def test_one_move(self):
        self.assertTrue(is_game('---------------------------OOO-----OOO-----OXO------X----------- X G6'))

    def test_two_move(self):
        self.assertTrue(is_game('---------------------------OOO-----OOO-----OXO------X----------- X G6 D7'))


class IsScoredGameTest(unittest.TestCase):
    
    def test_X_to_play(self):
        self.assertTrue(is_scored_game('OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO X C1 H1 +70 -02 +12'))

    def test_O_to_play(self):
        self.assertTrue(is_scored_game('OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO O C1 H1 +70 -02 +12'))
    
    def test_no_move(self):
        self.assertTrue(is_scored_game('OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO X'))
    
    def test_no_player(self):
        self.assertFalse(is_scored_game('OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO C1 H1 +70 -02 +12'))
