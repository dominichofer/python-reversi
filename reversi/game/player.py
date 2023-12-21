"Player interface and random player."
from abc import ABC, abstractmethod
from typing import Iterable
from random import choice
from reversi.board import Field, Position, possible_moves


class Player(ABC):
    "Player interface."

    @abstractmethod
    def choose_move(self, pos: Position) -> Field:
        "Chooses a move for a given position."

    @abstractmethod
    def choose_moves(self, pos: Iterable[Position]) -> list[Field]:
        "Chooses moves for given positions."


class RandomPlayer(Player):
    "A player that chooses a random move."

    def choose_move(self, pos: Position) -> Field:
        return choice(list(possible_moves(pos)))

    def choose_moves(self, pos: Iterable[Position]) -> list[Field]:
        return [self.choose_move(p) for p in pos]
