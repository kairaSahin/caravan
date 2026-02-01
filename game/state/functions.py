from game.moves.types import Move
from game.state.game_state import GameState, PlayerState


def get_move_player(state: GameState, move: Move) -> PlayerState | None:
	return state.players.get(move.player_id)
