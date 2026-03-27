from postgrest import APIError

from backend.api.errors import ErrorCode, PostgresErrorCode
from backend.api.functions.moves import step
from backend.api.functions.state import fetch_latest_game_state_with_game_id, insert_game_state, \
	game_state_to_player_exclusive_state
from backend.api.schemas.moves import MoveRequest, to_domain_move
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from backend.api.auth.jwt_utils import GamePlayerTokenPayload
from backend.api.deps import get_auth_payload, get_supabase
from backend.api.schemas.state import GameStatePlayerExclusiveResponse
from backend.shared.deserializers import payload_to_game_state
from game.player.enums import PlayerId

router = APIRouter(prefix="/moves", tags=["moves"])


# TODO: Add proper error handling and add other routes;

@router.post("/make_move/")
async def make_move(
		game_id: str,
		expected_state_version: int,
		move: MoveRequest,
		auth: GamePlayerTokenPayload = Depends(get_auth_payload),
		supabase: Client = Depends(get_supabase)):
	if auth["game_id"] != game_id:
		raise HTTPException(status_code=403, detail="Token/game mismatch")

	player_id = PlayerId(int(auth["player_id"]))
	domain_move = to_domain_move(move, player_id)

	try:
		result = fetch_latest_game_state_with_game_id(game_id, supabase)

		row = result.data

		if row is None:
			raise HTTPException(status_code=404, detail="Game state not found")

		state_payload = row["state"]
		current_state_version = row["state_version"]

		if expected_state_version != current_state_version:
			raise HTTPException(
				status_code=409,
				detail={
					"code": ErrorCode.STALE_STATE,
					"message": "State version mismatch",
					"expected_version": expected_state_version,
					"actual_version": current_state_version
				}
			)

		game_state = payload_to_game_state(state_payload)

		game_state = step(domain_move, game_state)

		inserted_row = insert_game_state(
			game_id=game_id,
			state=game_state,
			current_state_version=current_state_version,
			supabase_client=supabase
		)

		updated_state_payload = game_state_to_player_exclusive_state(inserted_row["state"], player_id)
		db_game_id = inserted_row["game_id"]
		db_version = inserted_row["state_version"]
	except HTTPException as exc:
		raise exc
	except APIError as exc:
		db_code = getattr(exc, "code", None)

		if db_code == PostgresErrorCode.UNIQUE_CONSTRAINT_VIOLATION:
			raise HTTPException(
				status_code=409,
				detail={
					"code": ErrorCode.STALE_STATE,
					"message": "State write conflict",
				},
			)
		raise HTTPException(
			status_code=500,
			detail={
				"code": ErrorCode.DB_ERROR,
				"message": f"Database error while processing move: {exc}",
			},
		)
	except KeyError as exc:
		raise HTTPException(
			status_code=500,
			detail={
				"code": ErrorCode.MALFORMED_STATE,
				"message": f"Malformed game state payload: missing key {exc.args[0]}"
			}
		)
	except Exception as exc:
		raise HTTPException(
			status_code=500,
			detail={
				"code": ErrorCode.UNEXPECTED_ERROR,
				"message": f"Unexpected error while building state response: {exc}"
			}
		)

	return GameStatePlayerExclusiveResponse(game_id=db_game_id, state_version=db_version, **updated_state_payload)
