"""Engine interface."""
from abc import ABC, abstractmethod
from typing import Iterable
from reversi.search import Field, Position, Result


class Engine(ABC):
    "Engine interface."

    @property
    @abstractmethod
    def name(self) -> str:
        "Returns the name of the engine."

    @abstractmethod
    def solve(self, pos: Position) -> Result:
        "Returns the solution of the position."

    @abstractmethod
    def solve_many(self, pos: Iterable[Position]) -> list[Result]:
        "Returns the solutions of the positions."

    @abstractmethod
    def choose_move(self, pos: Position) -> Field:
        "Returns the best move for the position."

    @abstractmethod
    def choose_moves(self, pos: Iterable[Position]) -> list[Field]:
        "Returns the best moves for the positions."
