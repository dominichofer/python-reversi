"Filtering functions for positions and scored positions."
from typing import Iterable
from reversi.board import Position
from .scored_position import ScoredPosition


def empty_count_filtered(arg: Iterable, empty_count: int) -> Iterable:
    """Filter an iterable of positions by empty count."""
    for x in arg:
        if isinstance(x, Position):
            if x.empty_count() == empty_count:
                yield x
        elif isinstance(x, ScoredPosition):
            if x.pos.empty_count() == empty_count:
                yield x


def empty_count_range_filtered(arg: Iterable, lower: int, upper: int) -> Iterable:
    """Filter an iterable of positions by empty count."""
    for x in arg:
        if isinstance(x, Position):
            if lower <= x.empty_count() <= upper:
                yield x
        elif isinstance(x, ScoredPosition):
            if lower <= x.pos.empty_count() <= upper:
                yield x
