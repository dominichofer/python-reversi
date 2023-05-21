# Interface
class HashTable:
    def insert(self, key, value) -> bool:
        pass

    def delete(self, key) -> bool:
        pass

    def look_up(self, key):
        "Returns value or None."
        pass

    def bucket(self, key):
        "Returns the bucket belonging to key."
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

    def bucket(self, key):
        return (key, None)

    def clear(self) -> None:
        pass


# Interface
class Storage:
    def __len__(self) -> int:
        pass

    def __setitem__(self, index: int, value) -> None:
        pass

    def __getitem__(self, index: int):
        pass


class SpecialKey_1Hash_HashTable(HashTable):
    """
    Hash table with:
    - fixed size
    - single hash function
    - 1 element per bucket
    - special 'empty_key' to mark a bucket as empty.
    """

    def __init__(self, storage: Storage, empty_key, hash_fkt=hash) -> None:
        self.storage: Storage = storage
        self.empty_key = empty_key
        self.hash_fkt = hash_fkt

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

    def delete(self, key) -> bool:
        h = self.__hash(key)
        stored_key, stored_value = self.storage[h]
        if stored_key == key:
            self.storage[h] = (self.empty_key, stored_value)
            return True
        else:
            return False

    def bucket(self, key):
        return self.storage[self.__hash(key)]

    def look_up(self, key):
        h = self.__hash(key)
        stored_key, stored_value = self.storage[h]
        if stored_key == key:
            return stored_value
        else:
            return None

    def clear(self) -> None:
        for i in range(len(self.storage)):
            _, stored_value = self.storage[i]
            self.storage[i] = (self.empty_key, stored_value)
