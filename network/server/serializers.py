import json

from game.state.game_state import GameState

# FIXME: Add proper game state serializer!
def serialize_game_state(state: GameState) -> str:
	state_dict = state.__dict__

	return json.dumps(state_dict)