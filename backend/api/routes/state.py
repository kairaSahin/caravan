from fastapi import APIRouter, Depends
from supabase import Client
from backend.api.deps import get_supabase
from backend.api.schemas.state import GameStateResponse

router = APIRouter(prefix="/state", tags=["state"])

# TODO: Add proper error handling and add other routes;

@router.get("/")
async def get_state(game_id: str, state_version: int, supabase: Client = Depends(get_supabase)) -> GameStateResponse:
	result = (
		supabase.table("game_states")
		.select("*")
		.eq("game_id", game_id)
		.eq("state_version", state_version)
		.single()
		.execute()
	)

	row = result.data

	state_payload = row["state"]
	db_game_id = row["game_id"]
	db_version = row["state_version"]

	return GameStateResponse(game_id=db_game_id, state_version=db_version, **state_payload)
