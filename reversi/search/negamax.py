"NegaMax search."
from reversi.game import Position, possible_moves, play, play_pass, end_score


class NegaMax:
    "NegaMax search."

    def __init__(self) -> None:
        self.nodes: int = 0

    def eval(self, pos: Position) -> int:
        "Evaluate a position."
        self.nodes += 1

        moves = possible_moves(pos)
        if not moves:
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.eval(passed)
            return end_score(pos)

        return max(-self.eval(play(pos, move)) for move in moves)
