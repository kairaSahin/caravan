from game.engine.loop import GetMoveFn, OnTurnStartFn, OnErrorFn, OnAppliedFn, OnGameEndFn
from game.moves.types import Move
from game.player.enums import PlayerId
from game.state.game_state import GameState, GameResult


def make_get_move_by_player(providers: dict[PlayerId, GetMoveFn]) -> GetMoveFn:
	def _get_move(state: GameState) -> Move:
		return providers[state.current_player](state)

	return _get_move


def make_on_turn_start_by_player(providers: dict[PlayerId, OnTurnStartFn]) -> OnTurnStartFn:
	def _on_turn_start(state: GameState) -> None:
		return providers[state.current_player](state)

	return _on_turn_start


def make_on_error_by_player(providers: dict[PlayerId, OnErrorFn]) -> OnErrorFn:
	def _on_error(state: GameState, err: str) -> None:
		return providers[state.current_player](state, err)

	return _on_error


def make_on_applied_by_player(providers: dict[PlayerId, OnAppliedFn]) -> OnAppliedFn:
	def _on_applied(state: GameState, move: Move) -> None:
		return providers[state.current_player](state, move)

	return _on_applied


def make_on_game_end_by_player(providers: dict[PlayerId, OnGameEndFn]) -> OnGameEndFn:
	def _on_game_end(state: GameState, game_result: GameResult) -> None:
		return providers[state.current_player](state, game_result)

	return _on_game_end
