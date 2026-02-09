from dataclasses import dataclass, field
from typing import Callable

from game.engine.apply import apply_move
from game.engine.exceptions import IllegalMove
from game.moves.types import Move
from game.state.enums import GamePhase
from game.state.game_state import GameResult, GameState


@dataclass(frozen=True)
class StepResult:
	game_result: GameResult | None = field(default=None)
	error: str | None = field(default=None)


# TODO: Check additional function callables if they are redundant/useless.
GetMoveFn = Callable[[GameState], Move]
OnTurnStartFn = Callable[[GameState], None]
OnErrorFn = Callable[[GameState, str], None]
OnAppliedFn = Callable[[GameState, Move], None]
OnGameEndFn = Callable[[GameState, GameResult], None]


def step(state: GameState, move: Move) -> StepResult:
	if state.game_phase == GamePhase.FINISHED:
		return StepResult(error=None)

	try:
		game_result = apply_move(state, move)
	except IllegalMove as e:
		return StepResult(error=str(e))

	if game_result is not None:
		return StepResult(game_result=game_result)

	return StepResult()


# Keyword argument force (*) added as future safety with optional function callables, so if some are removed, it is easier to adapt later on
def run(state: GameState, get_move: GetMoveFn, *,
		on_turn_start: OnTurnStartFn | None = None,
		on_error: OnErrorFn | None = None,
		on_applied: OnAppliedFn | None = None,
		on_game_end: OnGameEndFn | None = None, ) -> GameResult:
	while state.game_phase != GamePhase.FINISHED:
		if on_turn_start is not None:
			on_turn_start(state)

		move = get_move(state)

		step_result = step(state, move)

		if step_result.error is not None:
			if on_error is not None:
				on_error(state, step_result.error)

			continue

		if on_applied is not None:
			on_applied(state, move)

		if step_result.game_result is not None:
			if on_game_end is not None:
				on_game_end(state, step_result.game_result)

			return step_result.game_result

	raise RuntimeError("Game finished without returning a GameResult")
