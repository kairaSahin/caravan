from fastapi import APIRouter, Depends
from supabase import Client

from backend.api.deps import get_supabase
from backend.api.functions.games import host_game
from backend.api.schemas.games import HostGameResponse

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/host")
def host_lobby(supabase: Client = Depends(get_supabase)) -> HostGameResponse:
	return host_game(supabase)
