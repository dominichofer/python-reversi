import unittest
from reversi.board import *

class PlayTest(unittest.TestCase):

    def test_play(self):
        pos = play(Position.start(), Field(19))
        self.assertEqual(pos, Position(0x0000001000000000, 0x0000000818080000))

    def test_play_pass(self):
        start = Position.start()
        passed = play_pass(start)
        passed2 = play_pass(passed)
        self.assertNotEqual(start, passed)
        self.assertNotEqual(passed, passed2)
        self.assertEqual(start, passed2)
