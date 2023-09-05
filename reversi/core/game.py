import re
from .field import Field
from .position import Position, play, play_pass, possible_moves


class Game:
    def __init__(self, start: Position = Position.start(), moves = None):
        self.__start: Position = start
        self.__current: Position = start
        self.__moves: list[Field] = []
        if moves is not None:
            for move in moves:
                self.play(move)

    @staticmethod
    def from_string(string: str):
        # Example input:
        # 'OO-XXXX-OOOOOXX-OOOOXOXOOXOXOXXXOXOOOXXXOXOXOXXXOOXXXXXXOOOOOOOO O C1 h1'
        
        moves = None
        if len(string) > 67:
            moves = [Field[s] for s in string[67:].strip().split(' ')]
        return Game(Position.from_string(string), moves)

    def __str__(self) -> str:
        return f'{self.__start} {self.moves_string()}'
                
    def __eq__(self, o):
        return self.__start == o.__start and self.__moves == o.__moves

    @property
    def start_position(self) -> Position:
        return self.__start
    
    @property
    def current_position(self) -> Position:
        return self.__current
    
    @property
    def moves(self) -> list:
        return self.__moves
    
    def moves_string(self) -> list:
        return ' '.join(m.name for m in self.__moves)
    
    def is_over(self) -> bool:
        if possible_moves(self.__current):
            return False
        else:
            return not possible_moves(play_pass(self.__current))
        
    def positions(self):
        pos = self.__start
        yield pos
        for move in self.__moves:
            pos = play(pos, move)
            yield pos
            
    def statistics(self) -> str:
        P = self.__current.P.bit_count()
        O = self.__current.O.bit_count()
        E = self.__current.empties().bit_count()
        M = possible_moves(self.__current).bit_count()
        return f'Player: {P}\nOpponent: {O}\nEmpties: {E}\nMoves: {M}'

    def play(self, move: Field|str):
        if isinstance(move, str):
            move = Field[move]
        self.__moves.append(move)
        self.__current = play(self.__current, move)

    
def is_game(string: str):
    return re.fullmatch(r'[XO-]{64} [XO]( [A-H][1-8])*', string) is not None
