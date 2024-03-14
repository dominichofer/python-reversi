"Transformations of games and positions."
from typing import Iterable
from reversi.board import Position
from .game import Game
from .scored_game import ScoredGame
from .scored_position import ScoredPosition


def positions(arg) -> Iterable[Position]:
    """
    Returns a generator of positions from the argument.
    It can act on
    Game,
    ScoredGame,
    ScoredPosition,
    Iterable[Games],
    Iterable[ScoredGame],
    Iterable[ScoredPosition].
    """
    if isinstance(arg, Game):
        yield from arg.positions()
    elif isinstance(arg, ScoredGame):
        yield from positions(arg.game)
    elif isinstance(arg, ScoredPosition):
        yield arg.pos
    elif isinstance(arg, Iterable):
        for x in arg:
            yield from positions(x)
    else:
        raise TypeError(f"Cannot get positions from {type(arg)}")


def scores(arg) -> Iterable[int]:
    """
    Returns a generator of scores from the argument.
    It can act on
    ScoredGame,
    ScoredPosition,
    Iterable[ScoredGame],
    Iterable[ScoredPosition].
    """
    if isinstance(arg, ScoredGame):
        yield from arg.scores
    elif isinstance(arg, ScoredPosition):
        yield arg.score
    elif isinstance(arg, Iterable):
        for x in arg:
            yield from scores(x)


def scored_positions(*args) -> Iterable[ScoredPosition]:
    """
    Returns a generator of ScoredPositions from the arguments.
    It can act as
    scored_positions(ScoredGame),
    scored_positions(Iterable[ScoredGame]),
    scored_positions(Iterable[Position], Iterable[int]).
    """
    if len(args) == 1:
        arg = args[0]
        if isinstance(arg, ScoredGame):
            yield from scored_positions(arg.game.positions(), arg.scores)
        elif isinstance(arg, Iterable):
            for x in arg:
                yield from scored_positions(x)
    elif len(args) == 2:
        for pos, score in zip(args[0], args[1]):
            yield ScoredPosition(pos, score)
