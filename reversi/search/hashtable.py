"Hash table for storing search results."
from dataclasses import dataclass
from reversi.game import Position, intersection
from .search_result import SearchResult


@dataclass
class Bucket:
    "A bucket in a hash table."
    pos: Position = Position()
    result: SearchResult = SearchResult()

    def update(
        self,
        pos: Position,
        new_result: SearchResult,
    ) -> bool:
        "Update the bucket with a new result. Return whether the result was updated."
        if new_result.intensity > self.result.intensity:
            if pos == self.pos and new_result.intensity == self.result.intensity:
                self.result.best_move = new_result.best_move
                self.result.window = intersection(new_result.window, self.result.window)
            else:
                self.pos = pos
                self.result = new_result
            return True
        return False

    def look_up(self, pos: Position) -> SearchResult | None:
        "Return the result for a position or None."
        if pos == self.pos:
            return self.result
        return None

    def clear(self) -> None:
        "Clear the bucket."
        self.pos = Position()
        self.result = SearchResult()


class HashTable:
    "A hash table for storing search results."

    def __init__(self, size: int) -> None:
        self.buckets = [Bucket()] * size

    def update(self, pos: Position, new_result: SearchResult) -> bool:
        "Update the hash table with a new result. Return whether the result was updated."
        index = hash(pos) % len(self.buckets)
        return self.buckets[index].update(pos, new_result)

    def look_up(self, pos: Position) -> SearchResult | None:
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
