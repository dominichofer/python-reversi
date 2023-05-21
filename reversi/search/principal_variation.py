from enum import Enum
from dataclasses import dataclass
from reversi.core import *


class ResultType(Enum):
    fail_low = -1
    exact = 0
    fail_high = +1


@dataclass
class Result:
    score_type: ResultType
    score: int
    depth: int
    confidence_level: float
    best_move: Field

    @staticmethod
    def fail_low(score: int, depth: int, confidence_level: float, best_move: Field):
        return Result(ResultType.fail_low, score, depth, confidence_level, best_move)

    @staticmethod
    def exact(score: int, depth: int, confidence_level: float, best_move: Field):
        return Result(ResultType.exact, score, depth, confidence_level, best_move)

    @staticmethod
    def fail_high(score: int, depth: int, confidence_level: float, best_move: Field):
        return Result(ResultType.fail_high, score, depth, confidence_level, best_move)

    @staticmethod
    def end_score(pos: Position):
        return Result.exact(end_score(pos), pos.empty_count(), float('inf'), Field.PS)

    def is_fail_low(self) -> bool:
        return self.score_type == ResultType.fail_low

    def is_exact(self) -> bool:
        return self.score_type == ResultType.exact

    def is_fail_high(self) -> bool:
        return self.score_type == ResultType.fail_high

    @property
    def window(self) -> ClosedInterval:
        if self.is_fail_low():
            return ClosedInterval(-64, self.score)
        if self.is_exact():
            return ClosedInterval(self.score, self.score)
        if self.is_fail_high():
            return ClosedInterval(self.score, +64)

    def __neg__(self):
        return Result(ResultType(-self.score_type.value), -self.score, self.depth, self.confidence_level, self.best_move)

    def beta_cut(self, move: Field):
        return Result.fail_high(-self.score, self.depth + 1, self.confidence_level, move)


@dataclass
class Status:
    alpha: int
    best_score: int = -inf_score
    best_move: Field = Field.PS
    worst_confidence_level: float = float('inf')
    smallest_depth: int = 64

    def improve(self, result: Result, move: Field):
        self.worst_confidence_level = min(
            self.worst_confidence_level, result.confidence_level)
        self.smallest_depth = min(self.smallest_depth, result.depth + 1)
        if -result.score > self.best_score:
            self.best_score = -result.score
            self.best_move = move

    def result(self) -> Result:
        if self.best_score > self.alpha:
            return Result.exact(self.best_score, self.smallest_depth, self.worst_confidence_level, self.best_move)
        else:
            return Result.fail_low(self.best_score, self.smallest_depth, self.worst_confidence_level, self.best_move)


class PrincipalVariation:

    def __init__(self, tt=None, move_sorter=None, cutters: list = None) -> None:
        self.nodes = 0
        self.tt = tt or HashTableStub()
        self.sorted_moves = move_sorter or (lambda pos, *_: possible_moves(pos))
        self.cutters = cutters or []

    def eval(self, pos: Position, window: OpenInterval = None, depth: int = None, confidence_level: float = None) -> Result:
        return self.pvs(pos, window or OpenInterval(-inf_score, +inf_score), depth or pos.empty_count(), confidence_level or float('inf'))

    def pvs(self, pos: Position, window: OpenInterval, depth: int, confidence_level: float) -> Result:
        status = Status(window.lower)
        self.nodes += 1
        
        if not possible_moves(pos):
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.pvs(passed, -window, depth, confidence_level)
            return Result.end_score(pos)

        for cutter in self.cutters:
            ret = cutter(pos, window, depth, confidence_level)
            if ret is not None:
                return ret

        first = True
        for move in self.sorted_moves(pos, window, depth, confidence_level):
            if not first:
                zero_window = OpenInterval(window.lower, window.lower + 1)
                result = self.zws(play(pos, move), -zero_window, depth - 1, confidence_level)
                if -result.score < zero_window:
                    continue
                if -result.score > window:  # beta cut
                    ret = result.beta_cut(move)
                    self.tt.insert(pos, ret)
                    return ret

            result = self.pvs(play(pos, move), -window, depth - 1, confidence_level)
            if -result.score > window:  # beta cut
                ret = result.beta_cut(move)
                self.tt.insert(pos, ret)
                return ret
            status.improve(result, move)
            window.lower = max(window.lower, -result.score)
            first = False

        ret = status.result()
        self.tt.insert(pos, ret)
        return ret

    def zws(self, pos: Position, window: OpenInterval, depth: int, confidence_level: float) -> Result:
        status = Status(window.lower)
        self.nodes += 1
        
        if not possible_moves(pos):
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.zws(passed, -window, depth, confidence_level)
            return Result.end_score(pos)

        for cutter in self.cutters:
            ret = cutter(pos, window, depth, confidence_level)
            if ret is not None:
                return ret

        for move in self.sorted_moves(pos, window, depth, confidence_level):
            result = self.zws(play(pos, move), -window, depth - 1, confidence_level)
            if -result.score > window:  # beta cut
                ret = result.beta_cut(move)
                self.tt.insert(pos, ret)
                return ret
            status.improve(result, move)

        ret = status.result()
        self.tt.insert(pos, ret)
        return ret
