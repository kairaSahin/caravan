from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from backend.api.auth.jwt_utils import GamePlayerTokenPayload
from backend.api.deps import get_supabase, get_auth_payload
from backend.api.functions import fetch_game_state, game_state_to_player_exclusive_state
from backend.api.schemas.state import GameStateResponse, GameStatePlayerExclusiveResponse, GameStatePayload
from game.player.enums import PlayerId

router = APIRouter(prefix="/state", tags=["state"])


# TODO: Add proper error handling and add other routes;

@router.get("/")
async def get_state(game_id: str,
					state_version: int,
					auth: GamePlayerTokenPayload = Depends(get_auth_payload),
					supabase: Client = Depends(get_supabase)) -> GameStatePlayerExclusiveResponse:
	if auth["game_id"] != game_id:
		raise HTTPException(status_code=403, detail="Token/game mismatch")

	player_id = PlayerId(int(auth["player_id"]))

	result = fetch_game_state(game_id, state_version, supabase)

	row = result.data
	state_payload = game_state_to_player_exclusive_state(row["state"], player_id)
	db_game_id = row["game_id"]
	db_version = row["state_version"]

	return GameStatePlayerExclusiveResponse(game_id=db_game_id, state_version=db_version, **state_payload)


@router.get("/all")
async def get_complete_state(game_id: str, state_version: int,
							 supabase: Client = Depends(get_supabase)) -> GameStateResponse:
	result = fetch_game_state(game_id, state_version, supabase)

	row = result.data

	state_payload = row["state"]
	db_game_id = row["game_id"]
	db_version = row["state_version"]

	return GameStateResponse(game_id=db_game_id, state_version=db_version, **state_payload)
