# Interface
class Storage:
    def __len__(self) -> int:
        pass

    def __setitem__(self, index: int, value) -> None:
        pass

    def __getitem__(self, index: int):
        pass


# Interface
class HashTable:
    def insert(self, key, value) -> bool:
        pass

    def delete(self, key) -> bool:
        pass

    def look_up(self, key):
        "Returns value or None."
        pass

    def clear(self) -> None:
        pass


# Interface
class BinaryHashTable(HashTable):
    def insert(self, key: bytes, value: bytes) -> bool:
        pass

    def delete(self, key: bytes) -> bool:
        pass

    def look_up(self, key: bytes) -> bytes | None:
        "Returns value or None."
        pass

    def clear(self) -> None:
        pass


# Stub
class HashTableStub(HashTable):
    def insert(self, key, value) -> bool:
        return False
    
    def delete(self, key) -> bool:
        return False
    
    def look_up(self, key):
        return None

    def clear(self) -> None:
        pass


# Mock
class HashTableMock(HashTable):
    def __init__(self) -> None:
        self.dict = dict()

    def insert(self, key, value) -> bool:
        self.dict[key] = value
        return True
    
    def delete(self, key) -> bool:
        if key in self.dict:
            del self.dict[key]
            return True
        else:
            return False
    
    def look_up(self, key):
        return self.dict.get(key, None)

    def clear(self) -> None:
        self.dict.clear()
        
    
class SpecialKey_1Hash_HashTable(HashTable):
    """
    Hash table with:
    - fixed size
    - single hash function
    - 1 element per bucket
    - special 'empty_key' to mark a bucket as empty.
    """

    def __init__(self, storage: Storage, empty_key, hash_fkt=None) -> None:
        self.storage: Storage = storage
        self.empty_key = empty_key
        self.hash_fkt = hash_fkt or hash

    def __hash(self, key) -> int:
        return self.hash_fkt(key) % len(self.storage)

    def insert(self, key, value) -> bool:
        h = self.__hash(key)
        stored_key, _ = self.storage[h]
        if stored_key == self.empty_key or stored_key == key:
            self.storage[h] = (key, value)
            return True
        else:
            return False

    def delete(self, key: bytes) -> bool:
        h = self.__hash(key)
        stored_key, stored_value = self.storage[h]
        if stored_key == key:
            self.storage[h] = (self.empty_key, stored_value)
            return True
        else:
            return False

    def look_up(self, key: bytes) -> bytes | None:
        h = self.__hash(key)
   
        stored_key, stored_value = self.storage[h]
        if stored_key == key:         return stored_value
        else:
            return None

    def clear(self) -> None:
        for i in range(len(self.storage)):
            _, stored_value = self.storage[i]
            self.storage[i] = (self.empty_key, stored_value)


class HashtableCache(HashTable):
    "Write through"

    def __init__(self, caches: list[HashTable], hashtable: HashTable):
        self.caches = caches
        self.hashtable = hashtable

    def insert(self, key, value) -> bool:
        for ht in self.caches:
            ht.insert(key, value)
        return self.hashtable.insert(key, value)

    def delete(self, key) -> bool:
        for ht in self.caches:
            ht.delete(key)
        return self.hashtable.delete(key)

    def look_up(self, key):
        for ht in self.caches:
            value = ht.look_up(key)
            if value is not None:
                return value
        return self.hashtable.look_up(key)

    def clear(self) -> None:
        for ht in self.caches:
            ht.clear()
        self.hashtable.clear()


class BinaryHashtableAdapter(HashTable):
    def __init__(self, hashtable: BinaryHashTable, value_type) -> None:
        self.ht = hashtable
        self.value_type = value_type

    def insert(self, key, value) -> bool:
        return self.ht.insert(bytes(key), bytes(value))

    def delete(self, key) -> bool:
        return self.ht.delete(bytes(key))

    def look_up(self, key):
        ret = self.ht.look_up(bytes(key))
        if ret is None:
            return None
        else:
            return self.value_type.from_bytes(ret)

    def clear(self) -> None:
        self.ht.clear()
