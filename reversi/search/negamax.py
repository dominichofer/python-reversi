from reversi.core import *


class NegaMax:    def __init__(self, transposition_table: HashTable | None = None) -> None:
        self.nodes = 0
        self.tt = transposition_table or HashTableStub()

    def eval(self, pos: Position) -> int:
        self.nodes += 1

        moves = possible_moves(pos)
        if not moves:
            passed = play_pass(pos)
            if possible_moves(passed):
                return -self.eval(passed)
            return end_score(pos)

        t = self.tt.look_up(pos)
        if t is not None:
            return t

        score = max(-self.eval(play(pos, move)) for move in moves)

        self.tt.insert(pos, score)
        return score
