from enum import Enum
from dataclasses import dataclass
from multiprocessing.util import is_exiting
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

    def __str__(self) -> str:
        return f'{self.window} d{self.depth}@{self.confidence_level} {self.best_move.name}'

    def __neg__(self):
        "Negates the window and the result type"
        return Result(ResultType(-self.score_type.value), -self.score, self.depth, self.confidence_level, self.best_move)
    
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

    def beta_cut(self, move: Field):
        return Result.fail_high(-self.score, self.depth + 1, self.confidence_level, move)
    
    @staticmethod
    def from_bytes(b: bytes):
        score_type, score, depth, confidence_level, best_move = struct.unpack('bbBdB', b)
        return Result(ResultType(score_type), score, depth, confidence_level, Field(best_move))

    def __bytes__(self) -> bytes:
        return struct.pack('bbBdB', self.score_type.value, self.score, self.depth, self.confidence_level, self.best_move.value)


@dataclass
class Status:
    alpha: int
    best_score: int = -inf_score
    best_move: Field = Field.PS
    worst_confidence_level: float = float('inf')
    smallest_depth: int = 64

    def update(self, result: Result, move: Field):
        self.worst_confidence_level = min(self.worst_confidence_level, result.confidence_level)
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

    def transposition_cut(self, pos: Position, window: OpenInterval, depth: int, confidence_level: float):
        t = self.tt.look_up(pos)
        if t and t.depth >= depth and t.confidence_level >= confidence_level:
            if t.is_exact():
                return Result.exact(t.window.lower, t.depth, t.confidence_level, t.best_move)
            if t.window > window:
                return Result.fail_high(t.window.lower, t.depth, t.confidence_level, t.best_move)
            if t.window < window:
                return Result.fail_low(t.window.lower, t.depth, t.confidence_level, t.best_move)
        return None

    def pvs(self, pos: Position, window: OpenInterval, depth: int, confidence_level: float) -> Result:        
        self.nodes += 1
        
        if not possible_moves(pos):
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.pvs(passed, -window, depth, confidence_level)
            return Result.end_score(pos)

        if tc := self.transposition_cut(pos, window, depth, confidence_level):
            return tc

        for cutter in self.cutters:
            if ret := cutter(pos, window, depth, confidence_level):
                return ret

        status = Status(window.lower)
        first = True
        for move in self.sorted_moves(pos, window, depth, confidence_level):
            if not first:
                zero_window = OpenInterval(window.lower, window.lower + 1)
                result = self.zws(play(pos, move), -zero_window, depth - 1, confidence_level)
                if -result.score < zero_window:
                    status.update(result, move)
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
            status.update(result, move)
            window.lower = max(window.lower, -result.score)
            first = False

        ret = status.result()
        self.tt.insert(pos, ret)
        return ret

    def zws(self, pos: Position, window: OpenInterval, depth: int, confidence_level: float) -> Result:
        self.nodes += 1
        
        if not possible_moves(pos):
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.zws(passed, -window, depth, confidence_level)
            return Result.end_score(pos)
        
        if tc := self.transposition_cut(pos, window, depth, confidence_level):
            return tc

        for cutter in self.cutters:
            if ret := cutter(pos, window, depth, confidence_level):
                return ret
            
        status = Status(window.lower)
        for move in self.sorted_moves(pos, window, depth, confidence_level):
            result = self.zws(play(pos, move), -window, depth - 1, confidence_level)
            if -result.score > window:  # beta cut
                ret = result.beta_cut(move)
                self.tt.insert(pos, ret)
                return ret
            status.update(result, move)

        ret = status.result()
        self.tt.insert(pos, ret)
        return ret
