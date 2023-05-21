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

    @staticmethod
    def fail_low(score: int):
        return Result(ResultType.fail_low, score)

    @staticmethod
    def exact(score: int):
        return Result(ResultType.exact, score)
    
    @staticmethod
    def fail_high(score: int):
        return Result(ResultType.fail_high, score)

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


class AlphaBeta:
    "Fail-soft alpha-beta pruning"
    
    def __init__(self, tt = None, move_sorter = None) -> None:
        self.nodes = 0
        self.tt = tt or HashTableStub()
        self.sorted_moves = move_sorter or (lambda _, x: x)

    def eval(self, pos: Position, window: OpenInterval = None) -> int:
        window = window or OpenInterval(-inf_score, +inf_score)
        alpha = window.lower
        self.nodes += 1

        moves = possible_moves(pos)
        if not moves:
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.eval(passed, -window)
            return end_score(pos)

        t = self.tt.look_up(pos)
        if t is not None:
            if t.is_exact() or (t not in t.window):
                return t.score
        
        best_score = -inf_score
        for move in self.sorted_moves(pos, moves):
            score = -self.eval(play(pos, move), -window)
            if score > window: # beta cut
                self.tt.insert(pos, Result.fail_high(score))
                return score
            best_score = max(best_score, score)
            window.lower = max(window.lower, score)

        if best_score > alpha:
            self.tt.insert(pos, Result.exact(best_score))
        else:
            self.tt.insert(pos, Result.fail_low(best_score))
        return best_score
