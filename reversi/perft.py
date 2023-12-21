"Performance test functions."
from reversi.board import Position, play, play_pass, possible_moves


def __perft_1(pos: Position) -> int:
    "Perft function for depth 1."
    moves = possible_moves(pos)
    if moves:
        return len(moves)
    return 1 if possible_moves(play_pass(pos)) else 0


def perft(depth: int, pos: Position = Position.start()) -> int:
    "Perft function for any depth."

    if depth == 0:
        return 1
    if depth == 1:
        return __perft_1(pos)

    moves = possible_moves(pos)
    if depth == 2:
        if moves:
            return sum(__perft_1(play(pos, move)) for move in moves)
        return len(moves)

    if moves:
        return sum(perft(depth - 1, play(pos, move)) for move in moves)

    passed = play_pass(pos)
    if possible_moves(passed):
        return perft(depth - 1, passed)
    return 0
