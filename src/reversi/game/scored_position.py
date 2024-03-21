"A position with a score."

from dataclasses import dataclass
from reversi.board import Position
from .score import undefined_score


@dataclass
class ScoredPosition:
    "A position with a score."

    pos: Position
    score: int = undefined_score

    @staticmethod
    def from_string(string: str) -> "ScoredPosition":
        "Return a scored position from a string."
        # Example input:
        # 'OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO O % +02'
        score = int(string[69:])
        return ScoredPosition(Position.from_string(string), score)

    def __str__(self) -> str:
        return f"{self.pos} % {self.score:+03}"

    def __eq__(self, o) -> bool:
        return self.pos == o.pos and self.score == o.score

    def empty_count(self) -> int:
        "Returns the number of empty fields."
        return self.pos.empty_count()

    def is_score_defined(self) -> bool:
        "Returns whether the score is defined."
        return self.score != undefined_score
