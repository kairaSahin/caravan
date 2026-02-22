from game.player.enums import PlayerId
from game.state.enums import WinReason, GamePhase
from game.state.game_state import GameState, GameResult, PlayerState


def _payload_to_game_result(game_result: dict | None) -> GameResult | None:
	if game_result is None:
		return None

	return GameResult(
		winner_id=PlayerId(game_result['winner_id']),
		reason=WinReason(game_result['reason']) if game_result['reason'] is not None else None,
		end_turn_number=game_result['end_turn_number'],
	)


def _payload_to_current_player(player_id: int) -> PlayerId:
	return PlayerId(player_id)


def _payload_to_game_phase(game_phase: int) -> GamePhase:
	return GamePhase(game_phase)


def payload_to_game_state(payload: dict) -> GameState:
	return GameState(**payload)
