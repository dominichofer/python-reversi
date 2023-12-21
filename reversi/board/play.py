"Play a move on a position."
from numpy import uint64
from .field import Field, bit
from .position import Position


def flips_in_one_direction(pos: Position, x, y, dx, dy) -> uint64:
    "Returns the flips in one direction."
    bits = uint64(0)
    x += dx
    y += dy
    while (x >= 0) and (x < 8) and (y >= 0) and (y < 8):
        index = uint64(x * 8 + y)
        mask = uint64(1) << index
        if pos.opponent & mask:
            bits |= mask
        elif pos.player & mask:
            return bits
        else:
            break
        x += dx
        y += dy
    return uint64(0)


def flips(pos: Position, move: Field) -> uint64:
    "Returns the flipped fields for a move as a bitboard."
    x, y = divmod(move.value, 8)
    return flips_in_one_direction(pos, x, y, -1, -1) \
         | flips_in_one_direction(pos, x, y, -1, +0) \
         | flips_in_one_direction(pos, x, y, -1, +1) \
         | flips_in_one_direction(pos, x, y, +0, -1) \
         | flips_in_one_direction(pos, x, y, +0, +1) \
         | flips_in_one_direction(pos, x, y, +1, -1) \
         | flips_in_one_direction(pos, x, y, +1, +0) \
         | flips_in_one_direction(pos, x, y, +1, +1)


def play(pos: Position, move: Field) -> Position:
    "Returns the position after a move."
    if move == Field.PS:
        return play_pass(pos)
    else:
        bits = flips(pos, move)
        return Position(pos.opponent ^ bits, pos.player ^ bits ^ bit(move))


def play_pass(pos: Position) -> Position:
    "Returns the position after a pass."
    return Position(pos.opponent, pos.player)
