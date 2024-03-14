"Hash table for storing search results."

from reversi.game import Position
from .result import Result


class Bucket:
    "A bucket in a hash table."

    def __init__(self, pos: Position = Position(), result: Result = Result()):
        self.pos = pos
        self.result = result

    def update(
        self,
        pos: Position,
        new_result: Result,
    ) -> bool:
        "Update the bucket with a new result. Return whether the result was updated."
        self.pos = pos
        self.result = new_result
        return True

    def look_up(self, pos: Position) -> Result | None:
        "Return the result for a position or None."
        if pos == self.pos:
            return self.result
        return None

    def clear(self) -> None:
        "Clear the bucket."
        self.pos = Position()
        self.result = Result()


class HashTable:
    "A hash table for storing search results."

    def __init__(self, size: int) -> None:
        self.buckets = [Bucket()] * size

    def update(self, pos: Position, new_result: Result) -> bool:
        "Update the hash table with a new result. Return whether the result was updated."
        index = hash(pos) % len(self.buckets)
        return self.buckets[index].update(pos, new_result)

    def look_up(self, pos: Position) -> Result | None:
        "Return the result for a position or None."
        index = hash(pos) % len(self.buckets)
        return self.buckets[index].look_up(pos)

    def clear(self) -> None:
        "Clear the hash table."
        for bucket in self.buckets:
            bucket.clear()


class HashTableStub:
    "A stub for a hash table."

    def update(self, *_) -> bool:
        "Update the hash table with a new result. Return whether the result was updated."
        return False

    def look_up(self, *_) -> None:
        "Return the result for a position or None."

    def clear(self) -> None:
        "Clear the hash table."
