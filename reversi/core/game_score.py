import re
from .game import Game
from .field import Field
from .position import Position
from .score import undefined_score


class GameScore:
    def __init__(self, game: Game, scores = None):
        self.game = game
        if scores is None:
            self.clear_scores()
        else:
            self.scores = scores

    @staticmethod
    def from_string(string: str):
        # Example input:
        # 'OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO O C1 h1 +70 -02 +12'

        parts = string.strip().split(' ')
        pos = Position.from_string(string[:66])
        moves = []
        scores = []
        for part in parts[2:]:
            try:
                scores.append(int(part))
            except:
                moves.append(Field[part])
        return GameScore(Game(pos, moves), scores)

    def __str__(self) -> str:
        return ' '.join([str(self.game)] + [f'{s:+03}' for s in self.scores])
                
    def __eq__(self, o):
        return self.game == o.game and self.scores == o.scores

    def clear_scores(self):
        self.scores = [undefined_score] * (len(self.game.moves) + 1)
        

def is_game_score(string: str):
    return re.fullmatch(r'[XO-]{64} [XO]( [A-H][1-8])*( [+-][0-9][0-9])*', string) is not None
