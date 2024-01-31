"Search result."
from reversi.game import (
    ClosedInterval,
    Intensity,
    Field,
    min_score,
    max_score,
)


class Result:
    "Result of a search."

    def __init__(
        self,
        window: ClosedInterval = ClosedInterval(min_score, max_score),
        intensity: Intensity = Intensity(-1, 0.0),
        best_move: Field = Field.PS,
    ) -> None:
        self.window = window
        self.intensity = intensity
        self.best_move = best_move

    def __str__(self) -> str:
        return f"{self.window} d{self.intensity} {self.best_move.name}"

    def __neg__(self) -> "Result":
        return Result(-self.window, self.intensity, self.best_move)

    def is_exact(self) -> bool:
        "Return whether the result is exact."
        return self.window.lower == self.window.upper
