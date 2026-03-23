from fastapi import APIRouter, Depends, HTTPException
from postgrest import APIError
from supabase import Client

from backend.api.auth.jwt_utils import GamePlayerTokenPayload
from backend.api.deps import get_supabase, get_auth_payload
from backend.api.functions import fetch_game_state_with_game_id_and_state_ver, game_state_to_player_exclusive_state
from backend.api.schemas.state import GameStateResponse, GameStatePlayerExclusiveResponse
from game.player.enums import PlayerId

router = APIRouter(prefix="/state", tags=["state"])


@router.get("/")
async def get_state(game_id: str,
					state_version: int,
					auth: GamePlayerTokenPayload = Depends(get_auth_payload),
					supabase: Client = Depends(get_supabase)) -> GameStatePlayerExclusiveResponse:
	if auth["game_id"] != game_id:
		raise HTTPException(status_code=403, detail="Token/game mismatch")

	player_id = PlayerId(int(auth["player_id"]))

	try:
		result = fetch_game_state_with_game_id_and_state_ver(game_id, state_version, supabase)

		row = result.data

		if row is None:
			raise HTTPException(status_code=404, detail="Game state not found")

		state_payload = game_state_to_player_exclusive_state(row["state"], player_id)
		db_game_id = row["game_id"]
		db_version = row["state_version"]
	except (APIError, HTTPException) as exc:
		raise exc
	except KeyError as exc:
		raise HTTPException(status_code=500, detail=f"Malformed game state payload: missing key {exc.args[0]}")
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"Unexpected error while building state response: {exc}")

	return GameStatePlayerExclusiveResponse(game_id=db_game_id, state_version=db_version, **state_payload)


@router.get("/all")
async def get_complete_state(game_id: str, state_version: int,
							 supabase: Client = Depends(get_supabase)) -> GameStateResponse:
	try:
		result = fetch_game_state_with_game_id_and_state_ver(game_id, state_version, supabase)

		row = result.data

		if row is None:
			raise HTTPException(status_code=404, detail="Game state not found")

		state_payload = row["state"]
		db_game_id = row["game_id"]
		db_version = row["state_version"]
	except (APIError, HTTPException) as exc:
		raise exc
	except KeyError as exc:
		raise HTTPException(status_code=500, detail=f"Malformed game state payload: missing key {exc.args[0]}")
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"Unexpected error while building state response: {exc}")

	return GameStateResponse(game_id=db_game_id, state_version=db_version, **state_payload)
