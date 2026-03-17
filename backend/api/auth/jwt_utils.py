from typing import TypedDict

import jwt

from game.player.enums import PlayerId


class GamePlayerTokenPayload(TypedDict):
	game_id: str
	player_id: PlayerId


def create_game_player_token(game_id: str, player_id: PlayerId, secret_key: str, algorithm: str = "HS256") -> str:
	payload: GamePlayerTokenPayload = {
		"game_id": game_id,
		"player_id": player_id,
	}

	return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_game_player_token(token: str, secret_key: str, algorithm: str = "HS256") -> GamePlayerTokenPayload:
	payload = jwt.decode(token, secret_key, algorithms=[algorithm])

	game_id = payload.get("game_id")
	player_id = PlayerId(payload.get("player_id"))

	if not isinstance(game_id, str):
		raise ValueError("Invalid JWT payload: 'game_id' must be a string.")
	if not isinstance(player_id, PlayerId):
		raise ValueError("Invalid JWT payload: 'player_id' must be an enum of type PlayerId.")

	return {
		"game_id": game_id,
		"player_id": player_id,
	}
