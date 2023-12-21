"Game class for Reversi."
from reversi.board import Position, Field, play


class Game:
    "A game of Reversi starting from any position."

    def __init__(
        self, start: Position = Position.start(), moves: list[Field] | None = None
    ):
        self.__start: Position = start
        self.__moves: list[Field] = moves or []

    @staticmethod
    def from_string(string: str) -> "Game":
        "Return a game from a string."
        # Example input:
        # 'OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO O C1 H1'

        if len(string) > 67:
            moves = [Field[s] for s in string[67:].split(" ")]
        else:
            moves = None
        return Game(Position.from_string(string), moves)

    def __str__(self) -> str:
        moves = " ".join(move.name for move in self.__moves)
        return f"{self.__start} {moves}"

    def __eq__(self, o) -> bool:
        return self.__start == o.start_position and self.__moves == o.moves

    @property
    def start_position(self) -> Position:
        "Return the start position of the game."
        return self.__start

    @property
    def moves(self) -> list[Field]:
        "Return the moves played."
        return self.__moves

    def positions(self):
        "Return the positions of the game."
        pos = self.__start
        yield pos
        for move in self.__moves:
            pos = play(pos, move)
            yield pos

    def last_position(self) -> Position:
        "Return the last position of the game."
        *_, last = self.positions()
        return last

    def play(self, move: Field | str) -> None:
        "Advance the game by a move."
        if isinstance(move, str):
            move = Field[move]
        self.__moves.append(move)
