"A fail-soft alpha-beta search algorithm."
from reversi.game import (
    OpenInterval,
    Position,
    possible_moves,
    play,
    play_pass,
    end_score,
    min_score,
    max_score,
    inf_score,
)


class AlphaBeta:
    "Fail-soft alpha-beta search algorithm."

    def __init__(self, move_sorter=None) -> None:
        self.nodes = 0
        self.__sorted_moves = move_sorter or (lambda _, x: x)

    def eval(self, pos: Position, window: OpenInterval | None = None) -> int:
        "Evaluate a position."
        window = window or OpenInterval(min_score, max_score)
        self.nodes += 1

        moves = possible_moves(pos)
        if not moves:
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.eval(passed, -window)
            return end_score(pos)

        best_score = -inf_score
        for move in self.__sorted_moves(pos, moves):
            score = -self.eval(play(pos, move), -window)
            if score > window:  # beta cut
                return score
            best_score = max(best_score, score)
            window.lower = max(window.lower, score)
        return best_score
