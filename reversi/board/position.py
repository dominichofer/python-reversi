"Position on the board."
from typing import Iterable
from numpy import uint64
from .bitboard import (
    flipped_codiagonal as bb_flipped_codiagonal,
    flipped_diagonal as bb_flipped_diagonal,
    flipped_horizontal as bb_flipped_horizontal,
    flipped_vertical as bb_flipped_vertical,
)
from .field import Field


class Position:
    "Represents a position on the board."

    def __init__(self, player=0, opponent=0):
        self.__p = uint64(player)
        self.__o = uint64(opponent)

    @staticmethod
    def start():
        "Returns the starting position."
        return Position(0x0000000810000000, 0x0000001008000000)

    @staticmethod
    def from_string(string: str) -> "Position":
        "Returns a position from a string."
        # Example input:
        # 'OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO X'
        # 'OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO O'

        p = uint64(0)
        o = uint64(0)
        for i in range(64):
            if string[i] == "X":
                p |= uint64(1) << uint64(63 - i)
            if string[i] == "O":
                o |= uint64(1) << uint64(63 - i)

        if string[65] == "X":
            return Position(p, o)
        else:
            return Position(o, p)

    def __str__(self) -> str:
        return single_line_string(self)

    def __eq__(self, o):
        return self.player == o.player and self.opponent == o.opponent

    def __lt__(self, o):
        return self.player < o.player or (
            self.player == o.player and self.opponent < o.opponent
        )

    def __hash__(self):
        return hash((self.player, self.opponent))

    @property
    def player(self) -> uint64:
        "Returns the bitboard of the player."
        return self.__p

    @property
    def opponent(self) -> uint64:
        "Returns the bitboard of the opponent."
        return self.__o

    def player_at(self, field: Field) -> bool:
        "Returns whether the player has a disc at the given field."
        return self.player & (uint64(1) << uint64(field.value)) != uint64(0)

    def opponent_at(self, field: Field) -> bool:
        "Returns whether the opponent has a disc at the given field."
        return self.opponent & (uint64(1) << uint64(field.value)) != uint64(0)

    def discs(self) -> uint64:
        "Returns the bitboard of all discs."
        return self.player | self.opponent

    def empties(self) -> uint64:
        "Returns the bitboard of all empty fields."
        return ~self.discs()

    def empty_count(self) -> int:
        "Returns the number of empty fields."
        return self.empties().bit_count()


def single_line_string(pos: Position) -> str:
    "Returns a one line string representation."
    board = "".join(
        "X" if pos.player_at(Field(i)) else "O" if pos.opponent_at(Field(i)) else "-"
        for i in reversed(range(64))
    )
    return board + " X"


def multi_line_string(pos: Position) -> str:
    "Returns a multi line string representation."
    board = "  A B C D E F G H  \n"
    for i in reversed(range(8)):
        board += f"{8-i} "
        board += " ".join(
            "X"
            if pos.player_at(Field(i * 8 + j))
            else "O"
            if pos.opponent_at(Field(i * 8 + j))
            else "-"
            for j in reversed(range(8))
        )
        board += f" {8-i}\n"
    board += "  A B C D E F G H  "
    return board


def flipped_codiagonal(b: Position) -> Position:
    "Returns the position flipped along the codiagonal."
    return Position(bb_flipped_codiagonal(b.player), bb_flipped_codiagonal(b.opponent))


def flipped_diagonal(b: Position) -> Position:
    "Returns the position flipped along the diagonal."
    return Position(bb_flipped_diagonal(b.player), bb_flipped_diagonal(b.opponent))


def flipped_horizontal(b: Position) -> Position:
    "Returns the position flipped along the horizontal."
    return Position(bb_flipped_horizontal(b.player), bb_flipped_horizontal(b.opponent))


def flipped_vertical(b: Position) -> Position:
    "Returns the position flipped along the vertical."
    return Position(bb_flipped_vertical(b.player), bb_flipped_vertical(b.opponent))


def flipped_to_unique(pos1: Position) -> Position:
    "Returns a unique position from set of symmetric vaiants."
    pos2 = flipped_codiagonal(pos1)
    pos3 = flipped_diagonal(pos1)
    pos4 = flipped_horizontal(pos1)
    pos5 = flipped_vertical(pos1)
    pos6 = flipped_vertical(pos2)
    pos7 = flipped_vertical(pos3)
    pos8 = flipped_vertical(pos4)
    return min(pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8)


def unique_positions(positions: Iterable[Position]) -> set[Position]:
    "Returns a list of unique positions."
    return set(flipped_to_unique(pos) for pos in positions)


def end_score(pos: Position) -> int:
    "Returns the end score of a terminal position."
    p: int = pos.player.bit_count()
    o: int = pos.opponent.bit_count()
    if p > o:
        return 64 - 2 * o
    elif p < o:
        return 2 * p - 64
    else:
        return 0
