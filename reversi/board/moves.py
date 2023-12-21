"Possible moves and game over condition check."
from itertools import islice
from numpy import uint64
from reversi.base import cleared_lsb, countr_zero
from .field import Field, bit
from .position import Position
from .play import play_pass


class Moves(uint64):
    "Represents a set of moves."

    class Iterator:
        "Iterates over the moves."
        def __init__(self, b: uint64):
            self.b = b

        def __next__(self):
            if self.b == 0:
                raise StopIteration
            move = countr_zero(self.b)
            self.b = cleared_lsb(self.b)
            return Field(move)

    def __str__(self) -> str:
        return " ".join(move.name for move in self)

    def __new__(cls, b):
        return super(Moves, cls).__new__(cls, b)

    def __iter__(self):
        return self.Iterator(self)

    def __getitem__(self, index) -> int:
        return next(islice(self, index, None))

    def __len__(self) -> int:
        return self.bit_count()

    def __contains__(self, field: Field) -> bool:
        return self & bit(field) != 0


def possible_moves(pos: Position) -> Moves:
    "Returns all possible moves."
    pos_p = pos.player
    pos_o = pos.opponent
    mask0 = pos_o & uint64(0x7E7E7E7E7E7E7E7E)

    flip1 = mask0 & (pos_p << uint64(1))
    flip2 = mask0 & (pos_p >> uint64(1))
    flip3 = pos_o & (pos_p << uint64(8))
    flip4 = pos_o & (pos_p >> uint64(8))
    flip5 = mask0 & (pos_p << uint64(7))
    flip6 = mask0 & (pos_p >> uint64(7))
    flip7 = mask0 & (pos_p << uint64(9))
    flip8 = mask0 & (pos_p >> uint64(9))

    flip1 |= mask0 & (flip1 << uint64(1))
    flip2 |= mask0 & (flip2 >> uint64(1))
    flip3 |= pos_o & (flip3 << uint64(8))
    flip4 |= pos_o & (flip4 >> uint64(8))
    flip5 |= mask0 & (flip5 << uint64(7))
    flip6 |= mask0 & (flip6 >> uint64(7))
    flip7 |= mask0 & (flip7 << uint64(9))
    flip8 |= mask0 & (flip8 >> uint64(9))

    mask1 = mask0 & (mask0 << uint64(1))
    mask2 = mask1 >> uint64(1)
    mask3 = pos_o & (pos_o << uint64(8))
    mask4 = mask3 >> uint64(8)
    mask5 = mask0 & (mask0 << uint64(7))
    mask6 = mask5 >> uint64(7)
    mask7 = mask0 & (mask0 << uint64(9))
    mask8 = mask7 >> uint64(9)

    flip1 |= mask1 & (flip1 << uint64(2))
    flip2 |= mask2 & (flip2 >> uint64(2))
    flip3 |= mask3 & (flip3 << uint64(16))
    flip4 |= mask4 & (flip4 >> uint64(16))
    flip5 |= mask5 & (flip5 << uint64(14))
    flip6 |= mask6 & (flip6 >> uint64(14))
    flip7 |= mask7 & (flip7 << uint64(18))
    flip8 |= mask8 & (flip8 >> uint64(18))

    flip1 |= mask1 & (flip1 << uint64(2))
    flip2 |= mask2 & (flip2 >> uint64(2))
    flip3 |= mask3 & (flip3 << uint64(16))
    flip4 |= mask4 & (flip4 >> uint64(16))
    flip5 |= mask5 & (flip5 << uint64(14))
    flip6 |= mask6 & (flip6 >> uint64(14))
    flip7 |= mask7 & (flip7 << uint64(18))
    flip8 |= mask8 & (flip8 >> uint64(18))

    flip1 <<= uint64(1)
    flip2 >>= uint64(1)
    flip3 <<= uint64(8)
    flip4 >>= uint64(8)
    flip5 <<= uint64(7)
    flip6 >>= uint64(7)
    flip7 <<= uint64(9)
    flip8 >>= uint64(9)

    return Moves(
        pos.empties() & (flip1 | flip2 | flip3 | flip4 | flip5 | flip6 | flip7 | flip8)
    )


def mobility(pos: Position) -> int:
    "Returns the number of possible moves."
    return len(possible_moves(pos))


def is_game_over(pos: Position) -> bool:
    "Returns True if the game is over, False otherwise."
    if possible_moves(pos):
        return False
    elif possible_moves(play_pass(pos)):
        return False
    else:
        return True
