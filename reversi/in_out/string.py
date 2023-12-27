"Module for string recognition."
from re import fullmatch


def is_position(string: str) -> bool:
    "Returns whether the string is a valid position."
    return fullmatch(r"[XO-]{64} [XO]", string) is not None


def is_scored_position(string: str) -> bool:
    "Returns whether the string is a valid scored position."
    return fullmatch(r"[XO-]{64} [XO] % [+-]\d{1,2}", string) is not None


def is_game(string: str) -> bool:
    "Returns whether the string is a valid game."
    return fullmatch(r"[XO-]{64} [XO]( [A-H][1-8])*", string) is not None


def is_scored_game(string: str) -> bool:
    "Returns whether the string is a valid scored game."
    return (
        fullmatch(r"[XO-]{64} [XO]( [A-H][1-8])*( [+-][0-9][0-9])*", string) is not None
    )
