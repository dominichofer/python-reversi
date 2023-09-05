import unittest
from reversi import *


class SpecialKey_1Hash_HashTable_Test(unittest.TestCase):

    @staticmethod
    def empty_hashtable():
        return SpecialKey_1Hash_HashTable([(0, None)] * 8, 0)

    def test_insert(self):
        ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=1, value=2)) # can insert new key
        self.assertTrue(ht.insert(key=1, value=3)) # can insert on collision

    def test_delete(self):
        ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=1, value=2))
        self.assertTrue(ht.delete(key=1)) # can delete stored key
        self.assertFalse(ht.delete(key=1)) # cannot delete deleted key
        self.assertFalse(ht.delete(key=2)) # cannot delete unknown key

    def test_look_up(self):
        ht = self.empty_hashtable()
        ht.insert(key=1, value=2)
        self.assertEqual(ht.look_up(key=1), 2) # finds value to known key
        self.assertEqual(ht.look_up(key=2), None) # cannot find unknown key

    def test_clear(self):
        ht = self.empty_hashtable()
        ht.insert(key=1, value=2)
        ht.clear()
        self.assertEqual(ht.look_up(key=1), None) # cannot find unknown key


class HashtableCache_Test(unittest.TestCase):

    @staticmethod
    def empty_hashtable():
        L1 = HashTableMock()
        L2 = HashTableMock()
        L3 = HashTableMock()
        return L1, L2, L3, HashtableCache([L1, L2], L3)

    def test_insert(self):
        L1, L2, L3, ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=1, value=2)) # can insert new key
        self.assertTrue(ht.insert(key=1, value=3)) # can insert on collision

        self.assertEqual(L1.look_up(key=1), 3) # was written through
        self.assertEqual(L2.look_up(key=1), 3) # was written through
        self.assertEqual(L3.look_up(key=1), 3) # was written through
        self.assertEqual(ht.look_up(key=1), 3)

    def test_delete(self):
        L1, L2, L3, ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=1, value=2))
        self.assertTrue(ht.delete(key=1)) # can delete stored key
        self.assertFalse(ht.delete(key=1)) # cannot delete deleted key
        self.assertFalse(ht.delete(key=2)) # cannot delete unknown key

        self.assertFalse(L1.look_up(key=2)) # was written through
        self.assertFalse(L2.look_up(key=2)) # was written through
        self.assertFalse(L3.look_up(key=2)) # was written through
        self.assertFalse(ht.look_up(key=2))

    def test_look_up(self):
        L1, L2, L3, ht = self.empty_hashtable()
        ht.insert(key=1, value=2)
        self.assertEqual(ht.look_up(key=1), 2) # finds value to known key
        self.assertEqual(ht.look_up(key=2), None) # cannot find unknown key

        self.assertEqual(L1.look_up(key=2), None) # was written through
        self.assertEqual(L2.look_up(key=2), None) # was written through
        self.assertEqual(L3.look_up(key=2), None) # was written through

    def test_clear(self):
        L1, L2, L3, ht = self.empty_hashtable()
        ht.insert(key=1, value=2)
        ht.clear()
        self.assertEqual(L1.look_up(key=1), None) # cannot find unknown key
        self.assertEqual(L2.look_up(key=1), None) # cannot find unknown key
        self.assertEqual(L3.look_up(key=1), None) # cannot find unknown key
        self.assertEqual(ht.look_up(key=1), None) # cannot find unknown key


# Mock
class BinaryHashTable_TestingMock(HashTable):
    def __init__(self) -> None:
        self.dict = dict()

    def insert(self, key: bytes, value: bytes) -> bool:
        assert isinstance(key, bytes)
        assert isinstance(value, bytes)
        self.dict[key] = value
        return True

    def delete(self, key: bytes) -> bool:
        assert isinstance(key, bytes)
        if key in self.dict:
            del self.dict[key]
            return True
        else:
            return False

    def look_up(self, key: bytes) -> bytes | None:
        assert isinstance(key, bytes)
        return self.dict.get(key, None)

    def clear(self) -> None:
        self.dict.clear()


class BinaryHashtableAdapterTest(unittest.TestCase):

    @staticmethod
    def empty_hashtable():
        return BinaryHashtableAdapter(BinaryHashTable_TestingMock(), int)

    def test_insert(self):
        ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=1, value=2)) # can insert new key
        self.assertTrue(ht.insert(key=1, value=3)) # can insert on collision

    def test_delete(self):
        ht = self.empty_hashtable()
        self.assertTrue(ht.insert(key=1, value=2))
        self.assertTrue(ht.delete(key=1)) # can delete stored key
        self.assertFalse(ht.delete(key=1)) # cannot delete deleted key
        self.assertFalse(ht.delete(key=2)) # cannot delete unknown key

    def test_look_up(self):
        ht = self.empty_hashtable()
        ht.insert(key=1, value=2)
        self.assertEqual(ht.look_up(key=1), 2) # finds value to known key
        self.assertEqual(ht.look_up(key=2), None) # cannot find unknown key

    def test_clear(self):
        ht = self.empty_hashtable()
        ht.insert(key=1, value=2)
        ht.clear()
        self.assertEqual(ht.look_up(key=1), None) # cannot find unknown key


if __name__ == '__main__':
    unittest.main()
