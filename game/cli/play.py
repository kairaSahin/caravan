from numpy.random import default_rng

from game.cli.hooks import get_move_from_cli, on_turn_start_cli, on_error_cli
from game.engine.dynamic_hooks import make_get_move_by_player, make_on_turn_start_by_player, make_on_error_by_player
from game.engine.loop import run
from game.player.enums import PlayerId
from game.setup.deck_builder import build_standard_deck
from game.setup.game_config import GameConfig
from game.setup.game_initializer import init_game


def main() -> None:
	game_config = GameConfig(
		deck_builder=build_standard_deck,
		starting_hand_size=8,
		starting_player=PlayerId.P1,
		shuffle_decks=True,
		random_generator=default_rng(42)
	)

	state = init_game(game_config)

	get_move = make_get_move_by_player({
		PlayerId.P1: get_move_from_cli,
		PlayerId.P2: get_move_from_cli,
	})

	on_turn_start = make_on_turn_start_by_player({
		PlayerId.P1: on_turn_start_cli,
		PlayerId.P2: on_turn_start_cli,
	})

	on_error = make_on_error_by_player({
		PlayerId.P1: on_error_cli,
		PlayerId.P2: on_error_cli,
	})

	result = run(
		state=state,
		get_move=get_move,
		on_turn_start=on_turn_start,
		on_error=on_error,
	)

	print(f"\nGame over! Winner: {result.winner_id} | Reason: {result.reason.value} | End turn: {result.end_turn_number}")


if __name__ == "__main__":
	main()
