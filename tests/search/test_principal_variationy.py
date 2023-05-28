import unittest
from pathlib import Path
from reversi import *

endgame = read_file(Path(__file__) / '..' / '..' / '..' / 'data' / 'endgame.pos')
fforum = read_file(Path(__file__) / '..' / '..' / '..' / 'data' / 'fforum-1-19.pos')

class ResultTest(unittest.TestCase):
    def test_bytes(self):
        result = Result.fail_low(-2, 13, 1.3, Field.A7)
        self.assertEqual(Result.from_bytes(bytes(result)), result)


class PrincipalVariationTest(unittest.TestCase):
    def endgame_test(self, index: int):
        score = PrincipalVariation().eval(endgame[index].pos).score
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
        
    def endgame_fail_low_test(self, index: int):
        window = OpenInterval(endgame[index].score, +65)
        score = PrincipalVariation().eval(endgame[index].pos, window).score
        self.assertLessEqual(score, endgame[index].score)
        
    def test_endgame_fail_low_00(self): self.endgame_fail_low_test( 0)
    def test_endgame_fail_low_01(self): self.endgame_fail_low_test( 1)
    def test_endgame_fail_low_02(self): self.endgame_fail_low_test( 2)
    def test_endgame_fail_low_03(self): self.endgame_fail_low_test( 3)
    def test_endgame_fail_low_04(self): self.endgame_fail_low_test( 4)
    def test_endgame_fail_low_05(self): self.endgame_fail_low_test( 5)
    def test_endgame_fail_low_06(self): self.endgame_fail_low_test( 6)
    def test_endgame_fail_low_07(self): self.endgame_fail_low_test( 7)
    def test_endgame_fail_low_08(self): self.endgame_fail_low_test( 8)
    def test_endgame_fail_low_09(self): self.endgame_fail_low_test( 9)
    def test_endgame_fail_low_10(self): self.endgame_fail_low_test(10)
    def test_endgame_fail_low_11(self): self.endgame_fail_low_test(11)
    def test_endgame_fail_low_12(self): self.endgame_fail_low_test(12)
    def test_endgame_fail_low_13(self): self.endgame_fail_low_test(13)
    def test_endgame_fail_low_14(self): self.endgame_fail_low_test(14)
    def test_endgame_fail_low_15(self): self.endgame_fail_low_test(15)
    def test_endgame_fail_low_16(self): self.endgame_fail_low_test(16)
    def test_endgame_fail_low_17(self): self.endgame_fail_low_test(17)
    def test_endgame_fail_low_18(self): self.endgame_fail_low_test(18)
    def test_endgame_fail_low_19(self): self.endgame_fail_low_test(19)
    
    def endgame_fail_high_test(self, index: int):
        window = OpenInterval(-65, endgame[index].score)
        score = PrincipalVariation().eval(endgame[index].pos, window).score
        self.assertGreaterEqual(score, endgame[index].score)
        
    def test_endgame_fail_high_00(self): self.endgame_fail_high_test( 0)
    def test_endgame_fail_high_01(self): self.endgame_fail_high_test( 1)
    def test_endgame_fail_high_02(self): self.endgame_fail_high_test( 2)
    def test_endgame_fail_high_03(self): self.endgame_fail_high_test( 3)
    def test_endgame_fail_high_04(self): self.endgame_fail_high_test( 4)
    def test_endgame_fail_high_05(self): self.endgame_fail_high_test( 5)
    def test_endgame_fail_high_06(self): self.endgame_fail_high_test( 6)
    def test_endgame_fail_high_07(self): self.endgame_fail_high_test( 7)
    def test_endgame_fail_high_08(self): self.endgame_fail_high_test( 8)
    def test_endgame_fail_high_09(self): self.endgame_fail_high_test( 9)
    def test_endgame_fail_high_10(self): self.endgame_fail_high_test(10)
    def test_endgame_fail_high_11(self): self.endgame_fail_high_test(11)
    def test_endgame_fail_high_12(self): self.endgame_fail_high_test(12)
    def test_endgame_fail_high_13(self): self.endgame_fail_high_test(13)
    def test_endgame_fail_high_14(self): self.endgame_fail_high_test(14)
    def test_endgame_fail_high_15(self): self.endgame_fail_high_test(15)
    def test_endgame_fail_high_16(self): self.endgame_fail_high_test(16)
    def test_endgame_fail_high_17(self): self.endgame_fail_high_test(17)
    def test_endgame_fail_high_18(self): self.endgame_fail_high_test(18)
    def test_endgame_fail_high_19(self): self.endgame_fail_high_test(19)

    def test_fforum_01(self):
        empty_key = Position()
        storage = create_ram_storage(bytes(empty_key), b'0' * 13, 1_000_000)
        ht = SpecialKey_1Hash_HashTable(storage, bytes(empty_key))
        ht = BinaryHashtableAdapter(ht, Result)
        tt = Updating_HashTable(ht)
        sorter = mobility_and_tt_sorter(tt)
        cutters = [
            tt_cutter(tt),
            edax_cutter(r'G:\edax-ms-windows\edax-4.4', max_depth=13),
            ]
        score = PrincipalVariation(tt, sorter, cutters).eval(fforum[0].pos).score
        self.assertEqual(score, fforum[0].score)

if __name__ == '__main__':
    unittest.main(verbosity=2)
