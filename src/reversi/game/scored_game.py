"A game with scores for each move."
from reversi.board import Field, Position
from .game import Game
from .score import undefined_score


class ScoredGame:
    "A game with scores for each move."

    def __init__(self, game: Game, scores: list[int] | None = None):
        self.game = game
        self.scores = scores or [undefined_score] * (len(game.moves) + 1)

    @staticmethod
    def from_string(string: str) -> "ScoredGame":
        "Return a scored game from a string."
        # Example input:
        # 'OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO O C1 H1 +70 -02 +12'

        pos = Position.from_string(string)
        moves = []
        scores = []
        parts = string.split(" ")
        for part in parts[2:]:
            try:
                scores.append(int(part))
            except ValueError:
                moves.append(Field[part])
        return ScoredGame(Game(pos, moves), scores)

    def __str__(self) -> str:
        scores = " ".join(f"{s:+03}" for s in self.scores)
        return f"{self.game} {scores}"

    def __eq__(self, o):
        return self.game == o.game and self.scores == o.scores
