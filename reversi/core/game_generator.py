from .game import Game
from .position import Position, play
from .field import Field


def played_game(first_player, second_player, start: Position):
	game = Game(start)
	pos = Position(start)

	first_to_play = True
	pass_count = 0
	while pass_count < 2:
		player = first_player if first_to_play else second_player

		move: Field = player.choose_move(pos)
		pos = play(pos, move)

		if move == Field.PS:
			pass_count += 1
		else:
			game.play(move)
			pass_count = 0

		first_to_play = not first_to_play

	return game
