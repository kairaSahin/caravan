from fastapi import APIRouter

from game.moves.types import PlayCard

router = APIRouter(prefix="/moves", tags=["moves"])

# TODO: Add proper error handling and add other routes;

@router.post("/play_base/")
async def play_base_move(play_base: PlayCard):
    return {"message": "move received"}