from backend.api.schemas.moves import MoveRequest, to_domain_move
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from backend.api.auth.jwt_utils import GamePlayerTokenPayload
from backend.api.deps import get_auth_payload, get_supabase
from game.player.enums import PlayerId

router = APIRouter(prefix="/moves", tags=["moves"])


# TODO: Add proper error handling and add other routes;

@router.post("/make_move/")
async def make_move(
		game_id: str,
		move: MoveRequest,
		auth: GamePlayerTokenPayload = Depends(get_auth_payload),
		supabase: Client = Depends(get_supabase)):
	if auth["game_id"] != game_id:
		raise HTTPException(status_code=403, detail="Token/game mismatch")

	player_id = PlayerId(int(auth["player_id"]))
	domain_move = to_domain_move(move, player_id)

	# TODO: Handle make move here.

	return {"message": "move received"}
