"Move sorters."
from reversi.game import Position, Field, Moves, possible_moves, play
from .hashtable import HashTable


def sorted_by_mobility(pos: Position, moves: Moves):
    "Sort moves by mobility."
    return sorted(moves, key=lambda move: len(possible_moves(play(pos, move))))


def sorted_by_mobility_and_tt(tt: HashTable):
    "Sort moves by mobility and availability in the transposition table."

    def sorter(pos: Position, moves: Moves) -> list[Field]:
        t = tt.look_up(pos)
        tt_move = t.best_move if t else Field.PS
        return sorted(
            moves, key=lambda move: -1 if move == tt_move else len(possible_moves(play(pos, move)))
        )

    return sorter
