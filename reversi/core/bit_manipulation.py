def get_lsb(b):
    "Get least significant bit"
    return b & (~b + type(b)(1))

def cleared_lsb(b):
    "Cleared least significant bit"
    return b & (b - type(b)(1))

def countr_zero(b):
    "Number of consecutive 0 bits in the value of x, starting from the least significant bit"
    if b == 0:
        return 64
    return int(get_lsb(b)).bit_length() - 1
