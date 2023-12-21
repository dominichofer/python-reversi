"File input/output functions."
from typing import Iterable
from pathlib import Path
from reversi.game import Position, ScoredPosition, Game, ScoredGame
from .string import is_position, is_scored_position, is_game, is_scored_game


def __deserialize(string: str):
    if is_position(string):
        return Position.from_string(string)
    if is_scored_position(string):
        return ScoredPosition.from_string(string)
    if is_game(string):
        return Game.from_string(string)
    if is_scored_game(string):
        return ScoredGame.from_string(string)
    raise NotImplementedError


def read_file(file_path: Path | str) -> list:
    "Reads a file and returns a list of deserialized objects."
    if isinstance(file_path, str):
        file_path = Path(file_path)
    return [
        __deserialize(line)
        for line in file_path.read_text(encoding="utf-8").splitlines()
    ]


def write_file(file_path: Path | str, items: Iterable) -> None:
    "Writes a file with serialized objects."
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if not isinstance(items, Iterable):
        items = [items]
    file_path.write_text("\n".join(str(i) for i in items), encoding="utf-8")
