from reversi.core import Position, possible_moves, play, play_pass


def perft(depth: int, pos: Position = Position.start()) -> int:
    if depth == 0:
        return 1
    if depth == 1:
        return __perft_1(pos)
    return __perft(depth, pos)


def __perft_1(pos: Position) -> int:
    moves = possible_moves(pos)
    if moves:
        return len(moves)
    return 1 if possible_moves(play_pass(pos)) else 0


def __perft(depth: int, pos: Position) -> int:
    moves = possible_moves(pos)

    if depth == 2:
        if moves:
            return sum(__perft_1(play(pos, move)) for move in moves)
        return len(moves)

    if moves:
        return sum(__perft(depth - 1, play(pos, move)) for move in moves)

    passed = play_pass(pos)
    if possible_moves(passed):
        return __perft(depth - 1, passed)
    return 0
