from collections.abc import Iterable
from pathlib import Path
from reversi.core import *


def __deserialize(string: str):
    if is_position(string):
        return Position.from_string(string)
    if is_position_score(string):
        return PositionScore.from_string(string)
    if is_game(string):
        return Game.from_string(string)
    if is_game_score(string):
        return GameScore.from_string(string)
    raise NotImplementedError


def read_file(file_path: Path|str):
    if isinstance(file_path, str):
        file_path = Path(file_path)
        
    return [__deserialize(line) for line in file_path.read_text().strip().split('\n')]


def write_file(file_path: Path|str, items):
    if not isinstance(items, Iterable):
        items = [items]
        
    file_path.write_text('\n'.join(str(i) for i in items))
