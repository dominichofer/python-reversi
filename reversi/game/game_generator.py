"Module for generating games."
from typing import Iterable
from reversi.board import Position, Field, play
from .game import Game
from .player import Player


def played_game(first: Player, second: Player, start: Position) -> Game:
    "Play a game between two players."
    game = Game(start)
    pos = start

    first_to_play = True
    pass_count = 0
    while pass_count < 2:
        player = first if first_to_play else second

        move = player.choose_move(pos)
        pos = play(pos, move)

        if move == Field.PS:
            pass_count += 1
        else:
            game.play(move)
            pass_count = 0

        first_to_play = not first_to_play

    return game


def played_games(
    first: Player, second: Player, starts: Iterable[Position]
) -> list[Game]:
    "Play games between two players."
    games = [Game(pos) for pos in starts]
    pos = starts

    first_to_play = True
    pass_counts = [0] * len(games)
    while any(count < 2 for count in pass_counts):
        player = first if first_to_play else second

        moves = player.choose_moves(pos)
        pos = [play(p, m) for p, m in zip(pos, moves)]

        for i, move in enumerate(moves):
            if move == Field.PS:
                pass_counts[i] += 1
            else:
                games[i].play(move)
                pass_counts[i] = 0

        first_to_play = not first_to_play

    return games
