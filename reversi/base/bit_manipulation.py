"Bit Manipulation functions for bitboard operations"
from numpy import uint64, add, subtract


def get_lsb(b: uint64) -> uint64:
    "Get Least Significant Bit"
    return b & add(~b, uint64(1), dtype=uint64)


def cleared_lsb(b: uint64) -> uint64:
    "Removed Least Significant Bit"
    return b & subtract(b, uint64(1), dtype=uint64)


def countr_zero(b: uint64) -> int:
    "Number of consecutive 0 bits in the value of b, starting from the least significant bit"
    if b == 0:
        return 64
    return int(get_lsb(b)).bit_length() - 1
