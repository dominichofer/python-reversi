"Principal variation search."
from reversi.game import (
    OpenInterval,
    ClosedInterval,
    Intensity,
    Field,
    min_score,
    max_score,
    inf_score,
    Position,
    possible_moves,
    play,
    play_pass,
    end_score,
)
from .hashtable import HashTableStub
from .search_result import SearchResult


class Status:
    "Status of a search."

    def __init__(self, fail_low_limit: int) -> None:
        self.fail_low_limit = fail_low_limit
        self.best_score = -inf_score
        self.best_move = Field.PS
        self.lowest_intensity = Intensity(64)

    def update(self, result: SearchResult, move: Field):
        "Updates the status with the result of a move."
        self.lowest_intensity = Intensity(
            min(self.lowest_intensity.depth, result.intensity.depth + 1),
            min(
                self.lowest_intensity.confidence_level,
                result.intensity.confidence_level,
            ),
        )
        if -result.window > self.best_score:
            self.best_score = -result.window.upper
            self.best_move = move

    def result(self) -> SearchResult:
        "Returns the result of a completed search."
        if self.best_score > self.fail_low_limit:
            lower = self.best_score
        else:
            lower = min_score
        return SearchResult(
            ClosedInterval(lower, self.best_score),
            self.lowest_intensity,
            self.best_move,
        )


def beta_cut(result: SearchResult, move: Field) -> SearchResult:
    "Returns a beta cut result."
    return SearchResult(
        ClosedInterval(-result.window.upper, max_score), result.intensity + 1, move
    )


def end_result(pos: Position) -> SearchResult:
    "Returns the result of terminal position."
    s = end_score(pos)
    return SearchResult(ClosedInterval(s, s), Intensity(pos.empty_count()), Field.PS)


class PrincipalVariation:
    "Principal variation search."

    def __init__(
        self, move_sorter=None, transposition_table=None, cutters: list | None = None
    ) -> None:
        self.nodes = 0
        self.sorted_moves = move_sorter or (lambda _, x: x)
        self.tt = transposition_table or HashTableStub()
        self.cutters = cutters or []

    def eval(
        self,
        pos: Position,
        window: OpenInterval | None = None,
        intensity: Intensity | None = None,
    ) -> SearchResult:
        "Evaluate a position."
        return self.pvs(
            pos,
            window or OpenInterval(min_score, max_score),
            intensity or Intensity(pos.empty_count()),
        )

    def pvs(
        self, pos: Position, window: OpenInterval, intensity: Intensity
    ) -> SearchResult:
        "Principal variation search."
        self.nodes += 1

        moves = possible_moves(pos)
        if not moves:
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.pvs(passed, -window, intensity)
            return end_result(pos)

        for cutter in self.cutters:
            if cut := cutter(pos, window, intensity):
                return cut

        if tc := self.transposition_cut(pos, window, intensity):
            return tc

        status = Status(window.lower)
        first = True
        for move in self.sorted_moves(pos, moves):
            if not first:
                zero_window = OpenInterval(window.lower, window.lower + 1)
                result = self.zws(play(pos, move), -zero_window, intensity - 1)
                if -result.window < zero_window:
                    status.update(result, move)
                    continue
                if -result.window > window:  # beta cut
                    ret = beta_cut(result, move)
                    self.tt.update(pos, ret)
                    return ret

            result = self.pvs(play(pos, move), -window, intensity - 1)
            if -result.window > window:  # beta cut
                ret = beta_cut(result, move)
                self.tt.update(pos, ret)
                return ret
            status.update(result, move)
            window.lower = max(window.lower, -result.window.upper)
            first = False

        ret = status.result()
        self.tt.update(pos, ret)
        return ret

    def zws(
        self, pos: Position, window: OpenInterval, intensity: Intensity
    ) -> SearchResult:
        "Zero-window search."
        self.nodes += 1

        moves = possible_moves(pos)
        if not moves:
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.zws(passed, -window, intensity)
            return end_result(pos)

        for cutter in self.cutters:
            if ret := cutter(pos, window, intensity):
                return ret

        if tc := self.transposition_cut(pos, window, intensity):
            return tc

        status = Status(window.lower)
        for move in self.sorted_moves(pos, moves):
            result = self.zws(play(pos, move), -window, intensity - 1)
            if -result.window > window:  # beta cut
                ret = beta_cut(result, move)
                self.tt.update(pos, ret)
                return ret
            status.update(result, move)

        ret = status.result()
        self.tt.update(pos, ret)
        return ret

    def transposition_cut(
        self, pos: Position, window: OpenInterval, intensity: Intensity
    ) -> SearchResult | None:
        "Returns a transposition cut result if one fits. None otherwise."
        t = self.tt.look_up(pos)
        if t and t.intensity >= intensity:
            if t.is_exact() or t.window > window or t.window < window:
                return t
        return None
