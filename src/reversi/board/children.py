"Children of a position."
from .position import Position
from .play import play, play_pass
from .moves import possible_moves


def children(pos: Position, plies: int, pass_is_a_ply: bool = False):
    "Returns the children of a position."
    if plies == 0:
        yield pos
    else:
        moves = possible_moves(pos)
        if moves:
            for move in moves:
                yield from children(play(pos, move), plies - 1, pass_is_a_ply)
        else:
            passed = play_pass(pos)
            if possible_moves(passed):
                yield from children(
                    passed, (plies - 1) if pass_is_a_ply else plies, pass_is_a_ply
                )
