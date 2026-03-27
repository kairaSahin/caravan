from fastapi import HTTPException

from backend.api.errors import ErrorCode
from game.engine.apply import apply_move
from game.engine.exceptions import IllegalMove
from game.moves.types import Move
from game.state.enums import GamePhase
from game.state.game_state import GameState


def step(move: Move, state: GameState) -> GameState:
	if state.game_phase == GamePhase.FINISHED:
		raise HTTPException(
			status_code=400,
			detail={
				"code": ErrorCode.FINISHED_GAME,
				"message": "Cannot make a move on a finished game."
			}
		)

	try:
		game_result = apply_move(state, move)
	except IllegalMove as exc:
		raise HTTPException(
			status_code=400,
			detail={
				"code": ErrorCode.ILLEGAL_MOVE,
				"message": str(exc)
			}
		)

	if game_result is not None:
		state.game_result = game_result


	return state