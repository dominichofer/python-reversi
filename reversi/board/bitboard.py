from numpy import uint64


def flipped_codiagonal(b: uint64) -> uint64:
    """
    # # # # # # # /
    # # # # # # / #
    # # # # # / # #
    # # # # / # # #
    # # # / # # # #
    # # / # # # # #
    # / # # # # # #
    / # # # # # # # <-LSB
    """
    t = b ^ (b << uint64(36))
    b ^= (t ^ (b >> uint64(36))) & uint64(0xF0F0F0F00F0F0F0F)
    t = (b ^ (b << uint64(18))) & uint64(0xCCCC0000CCCC0000)
    b ^= t ^ (t >> uint64(18))
    t = (b ^ (b << uint64(9))) & uint64(0xAA00AA00AA00AA00)
    b ^= t ^ (t >> uint64(9))
    return b


def flipped_diagonal(b: uint64) -> uint64:
    r"""
    \ # # # # # # #
    # \ # # # # # #
    # # \ # # # # #
    # # # \ # # # #
    # # # # \ # # #
    # # # # # \ # #
    # # # # # # \ #
    # # # # # # # \ <-LSB
    """
    t = (b ^ (b >> uint64(7))) & uint64(0x00AA00AA00AA00AA)
    b ^= t ^ (t << uint64(7))
    t = (b ^ (b >> uint64(14))) & uint64(0x0000CCCC0000CCCC)
    b ^= t ^ (t << uint64(14))
    t = (b ^ (b >> uint64(28))) & uint64(0x00000000F0F0F0F0)
    b ^= t ^ (t << uint64(28))
    return b


def flipped_horizontal(b: uint64) -> uint64:
    """
    # # # #|# # # #
    # # # #|# # # #
    # # # #|# # # #
    # # # #|# # # #
    # # # #|# # # #
    # # # #|# # # #
    # # # #|# # # #
    # # # #|# # # # <-LSB
    """
    b = ((b >> uint64(1)) & uint64(0x5555555555555555)) | (
        (b << uint64(1)) & uint64(0xAAAAAAAAAAAAAAAA)
    )
    b = ((b >> uint64(2)) & uint64(0x3333333333333333)) | (
        (b << uint64(2)) & uint64(0xCCCCCCCCCCCCCCCC)
    )
    b = ((b >> uint64(4)) & uint64(0x0F0F0F0F0F0F0F0F)) | (
        (b << uint64(4)) & uint64(0xF0F0F0F0F0F0F0F0)
    )
    return b


def flipped_vertical(b: uint64) -> uint64:
    """
    # # # # # # # #
    # # # # # # # #
    # # # # # # # #
    # # # # # # # #
    ---------------
    # # # # # # # #
    # # # # # # # #
    # # # # # # # #
    # # # # # # # # <-LSB
    """
    b = ((b >> uint64(32)) & uint64(0x00000000FFFFFFFF)) | (
        (b << uint64(32)) & uint64(0xFFFFFFFF00000000)
    )
    b = ((b >> uint64(16)) & uint64(0x0000FFFF0000FFFF)) | (
        (b << uint64(16)) & uint64(0xFFFF0000FFFF0000)
    )
    b = ((b >> uint64(8)) & uint64(0x00FF00FF00FF00FF)) | (
        (b << uint64(8)) & uint64(0xFF00FF00FF00FF00)
    )
    return b
