from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from backend.api.auth.jwt_utils import GamePlayerTokenPayload
from backend.api.deps import get_supabase, get_auth_payload
from backend.api.functions.state import handle_state_fetch
from backend.api.schemas.state import GameStateResponse, GameStatePlayerExclusiveResponse
from game.player.enums import PlayerId

router = APIRouter(prefix="/state", tags=["state"])


@router.get("/")
async def get_state(game_id: str,
					auth: GamePlayerTokenPayload = Depends(get_auth_payload),
					supabase: Client = Depends(get_supabase)) -> GameStatePlayerExclusiveResponse:
	if auth["game_id"] != game_id:
		raise HTTPException(status_code=403, detail="Token/game mismatch")

	player_id = PlayerId(int(auth["player_id"]))

	db_game_id, db_version, state_payload = handle_state_fetch(
		game_id=game_id,
		player_id=player_id,
		is_player_exclusive=True,
		supabase_client=supabase
	)

	return GameStatePlayerExclusiveResponse(game_id=db_game_id, state_version=db_version, **state_payload)


@router.get("/all")
async def get_complete_state(game_id: str,
							 supabase: Client = Depends(get_supabase)) -> GameStateResponse:
	db_game_id, db_version, state_payload = handle_state_fetch(
		game_id=game_id,
		player_id=None,
		is_player_exclusive=False,
		supabase_client=supabase
	)

	return GameStateResponse(game_id=db_game_id, state_version=db_version, **state_payload)
