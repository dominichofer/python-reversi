import unittest
from pathlib import Path
from reversi import *

endgame = read_file(Path(__file__).parent / '..' / '..' / 'data' / 'endgame.pos')


class ParallelTreeTest(unittest.TestCase):
    
    def assertNextTasks(self, tree, tasks):
        tree_tasks = tree.get_tasks()
        self.assertEqual([t.pos for t in tree_tasks], tasks)
        for t in tree_tasks:
            tree.report(t, result=0)

    def test_get_tasks(self):
        def move_sorter(pos):
            return ['A', 'B', 'C', 'D']
        def play(pos, move):
            return pos + move
        
        tree = ParallelTree(3, '', OpenInterval(-1, 1), move_sorter, play)
        
        self.assertNextTasks(tree, ['AAA'])
        self.assertNextTasks(tree, ['AAB', 'AAC', 'AAD'])
        self.assertNextTasks(tree, ['ABA', 'ACA', 'ADA'])
        self.assertNextTasks(tree, ['ABB', 'ACB', 'ADB'])
        self.assertNextTasks(tree, ['ABC', 'ABD', 'ACC', 'ACD', 'ADC', 'ADD'])
        self.assertNextTasks(tree, ['BAA', 'BAB', 'BAC', 'BAD', 'CAA', 'CAB', 'CAC', 'CAD', 'DAA', 'DAB', 'DAC', 'DAD'])
        self.assertNextTasks(tree, ['BBA', 'BBB', 'BBC', 'BBD', 'CBA', 'CBB', 'CBC', 'CBD', 'DBA', 'DBB', 'DBC', 'DBD'])
        self.assertNextTasks(tree, ['BCA', 'BCB', 'BCC', 'BCD', 'BDA', 'BDB', 'BDC', 'BDD', 'CCA', 'CCB', 'CCC', 'CCD', 'CDA', 'CDB', 'CDC', 'CDD', 'DCA', 'DCB', 'DCC', 'DCD', 'DDA', 'DDB', 'DDC', 'DDD'])        
        self.assertTrue(tree.is_solved)
        

class DynamicTreeSearchTest(unittest.TestCase):
    def endgame_test(self, index: int):
        score = DynamicTreeSearch(3, PrincipalVariation()).eval(endgame[index].pos)
        self.assertEqual(score, endgame[index].score)

    def test_endgame_00(self): self.endgame_test( 0)
    def test_endgame_01(self): self.endgame_test( 1)
    def test_endgame_02(self): self.endgame_test( 2)
    def test_endgame_03(self): self.endgame_test( 3)
    def test_endgame_04(self): self.endgame_test( 4)
    def test_endgame_05(self): self.endgame_test( 5)
    def test_endgame_06(self): self.endgame_test( 6)
    def test_endgame_07(self): self.endgame_test( 7)
    def test_endgame_08(self): self.endgame_test( 8)
    def test_endgame_09(self): self.endgame_test( 9)
    def test_endgame_10(self): self.endgame_test(10)
    def test_endgame_11(self): self.endgame_test(11)
    def test_endgame_12(self): self.endgame_test(12)
    def test_endgame_13(self): self.endgame_test(13)
    def test_endgame_14(self): self.endgame_test(14)
    def test_endgame_15(self): self.endgame_test(15)
    def test_endgame_16(self): self.endgame_test(16)
    def test_endgame_17(self): self.endgame_test(17)
    def test_endgame_18(self): self.endgame_test(18)
    def test_endgame_19(self): self.endgame_test(19)

if __name__ == '__main__':
    unittest.main(verbosity=2)
