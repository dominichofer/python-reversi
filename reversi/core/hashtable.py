# Interface
class Storage:
    def __len__(self) -> int:
        pass

    def __setitem__(self, index: int, value: bytes) -> None:
        pass

    def __getitem__(self, index: int) -> bytes:
        pass


def create_ram_storage(init_key: bytes, init_value: bytes, count: int) -> bytes:
    return [b''.join([init_key, init_value])] * count


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

    
class SpecialKey_1Hash_HashTable(BinaryHashTable):
    """
    Hash table with:
    - fixed size
    - single hash function
    - 1 element per bucket
    - special 'empty_key' to mark a bucket as empty.
    """

    def __init__(self, storage: Storage, empty_key: bytes, hash_fkt=None) -> None:
        self.storage: Storage = storage
        self.empty_key = empty_key
        self.key_len = len(self.empty_key)
        self.hash_fkt = hash_fkt or hash

    def __hash(self, key: bytes) -> int:
        return self.hash_fkt(key) % len(self.storage)

    def _split(self, value: bytes) -> tuple[bytes]:
        return value[:self.key_len], value[self.key_len:]

    def _join(self, key: bytes, value: bytes) -> bytes:
        return b''.join([key, value])

    def insert(self, key: bytes, value: bytes) -> bool:
        h = self.__hash(key)
        stored_key, _ = self._split(self.storage[h])
        if stored_key == self.empty_key or stored_key == key:
            self.storage[h] = self._join(key, value)
            return True
        else:
            return False

    def delete(self, key: bytes) -> bool:
        h = self.__hash(key)
        stored_key, stored_value = self._split(self.storage[h])
        if stored_key == key:
            self.storage[h] = self._join(self.empty_key, stored_value)
            return True
        else:
            return False

    def look_up(self, key: bytes) -> bytes | None:
        h = self.__hash(key)
        stored_key, stored_value = self._split(self.storage[h])
        if stored_key == key:
            return stored_value
        else:
            return None

    def clear(self) -> None:
        for i in range(len(self.storage)):
            _, stored_value = self._split(self.storage[i])
            self.storage[i] = self._join(self.empty_key, stored_value)


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
