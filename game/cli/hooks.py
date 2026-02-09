from game.cli.menu import choose_action_menu
from game.cli.printer import print_game_state, print_applied_moves
from game.moves.types import Move
from game.state.game_state import GameState


def get_move_from_cli(state: GameState) -> Move:
	return choose_action_menu(state)


def on_turn_start_cli(state: GameState) -> None:
	print_game_state(state)


def on_applied_cli(state: GameState, move: Move) -> None:
	print_applied_moves(state, move)
