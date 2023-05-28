import unittest
from reversi import *


class SpecialKey_1Hash_HashTable_Test(unittest.TestCase):

    @staticmethod
    def empty_hashtable():
        return SpecialKey_1Hash_HashTable(create_ram_storage(b'0000', b'00', 8), b'0000')

    def test_insert(self):
        ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=b'0001', value=b'02')) # can insert new key
        self.assertTrue(ht.insert(key=b'0001', value=b'03')) # can insert on collision

    def test_delete(self):
        ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=b'0001', value=b'02'))
        self.assertTrue(ht.delete(key=b'0001')) # can delete stored key
        self.assertFalse(ht.delete(key=b'0001')) # cannot delete deleted key
        self.assertFalse(ht.delete(key=b'0002')) # cannot delete unknown key

    def test_look_up(self):
        ht = self.empty_hashtable()
        ht.insert(key=b'0001', value=b'02')
        self.assertEqual(ht.look_up(key=b'0001'), b'02') # finds value to known key
        self.assertEqual(ht.look_up(key=b'0002'), None) # cannot find unknown key

    def test_clear(self):
        ht = self.empty_hashtable()
        ht.insert(key=b'0001', value=b'02')
        ht.clear()
        self.assertEqual(ht.look_up(key=b'0001'), None) # cannot find unknown key


if __name__ == '__main__':
    unittest.main()
