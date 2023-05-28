from reversi.core import *
from reversi.engine.edax import Edax
from .principal_variation import Result, PrincipalVariation


class Updating_HashTable(HashTable):
    """
    HashTable decorator with:
      1 element per bucket
    """

    def __init__(self, ht: HashTable) -> None:
        self.ht: HashTable = ht

    def insert(self, key: Position, value: Result) -> bool:
        stored_value = self.ht.look_up(key)
        if (
            stored_value is not None
            and value.depth >= stored_value.depth
            and stored_value.confidence_level >= value.confidence_level
        ):
            self.ht.delete(key)
        return self.ht.insert(key, value)

    def delete(self, key: Position) -> bool:
        return self.ht.delete(key)

    def bucket(self, key: Position):
        return self.ht.bucket(key)

    def look_up(self, key: Position) -> Result:
        return self.ht.look_up(key)

    def clear(self) -> None:
        self.ht.clear()


def tt_cutter(tt: HashTable):
    def cutter(pos: Position, window: OpenInterval, depth: int, confidence_level: float) -> Result | None:
        t = tt.look_up(pos)
        if (
            t is not None
            and t.depth >= depth
            and t.confidence_level >= confidence_level
            and (t.is_exact() or not t.window.overlaps(window))
        ):
            return t
        return None

    return cutter


def edax_cutter(exe_path, min_depth: int = 12, max_depth: int = 64):
    def cutter(pos: Position, window: OpenInterval, depth: int, confidence_level: float) -> Result | None:
        if depth < min_depth or depth > max_depth:
            return None
        line = Edax(exe_path, level=depth).solve(pos)[0]
        return Result.exact(line.score, line.depth, line.confidence_level, line.pv[0] if len(line.pv) > 1 else Field.PS)

    return cutter


def sorted_by_mobility(pos: Position, window: OpenInterval, depth: int, confidence_level: float) -> Moves:
    return sorted(
        possible_moves(pos),
        key=lambda move: mobility(play(pos, move))
    )

def mobility_and_tt_sorter(tt: HashTable):
    def sorter(pos: Position, window: OpenInterval, depth: int, confidence_level: float) -> Moves:
        t = tt.look_up(pos)
        if t is None:
            tt_move = Field.PS
        else:
            tt_move = t.best_move
        return sorted(
            possible_moves(pos),
            key=lambda move: -1 if move == tt_move else mobility(play(pos, move))
        )
    return sorter
