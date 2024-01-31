"Search result."
from dataclasses import dataclass
from reversi.game import (
    ClosedInterval,
    Intensity,
    Field,
    min_score,
    max_score,
)


@dataclass
class Result:
    "Result of a search."
    window: ClosedInterval = ClosedInterval(min_score, max_score)
    intensity: Intensity = Intensity(-1, 0.0)
    best_move: Field = Field.PS

    def __str__(self) -> str:
        return f"{self.window} d{self.intensity} {self.best_move.name}"

    def __neg__(self) -> "Result":
        return Result(-self.window, self.intensity, self.best_move)

    def is_exact(self) -> bool:
        "Return whether the result is exact."
        return self.window.lower == self.window.upper
