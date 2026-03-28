import os
from datetime import timedelta, timezone, datetime
from typing import TypedDict

import jwt
from dotenv import load_dotenv

from game.player.enums import PlayerId

load_dotenv()


class EncodedGamePlayerTokenPayload(TypedDict):
	game_id: str
	player_id: int
	iat: int
	exp: int


class GamePlayerTokenPayload(TypedDict):
	game_id: str
	player_id: PlayerId
	iat: int
	exp: int


def create_game_player_token(
		game_id: str,
		player_id: PlayerId,
		secret_key: str,
		algorithm: str = "HS256",
		expires_in: timedelta | None = None,
) -> str:
	if expires_in is None:
		expires_in = timedelta(hours=int(os.environ.get("JWT_EXPIRES_IN_HOURS", "24")))

	now = datetime.now(timezone.utc)

	payload: EncodedGamePlayerTokenPayload = {
		"game_id": game_id,
		"player_id": int(player_id),
		"iat": int(now.timestamp()),
		"exp": int((now + expires_in).timestamp()),
	}

	return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_game_player_token(token: str, secret_key: str, algorithm: str = "HS256") -> GamePlayerTokenPayload:
	payload = jwt.decode(
		token,
		secret_key,
		algorithms=[algorithm],
		options={"require": ["exp", "iat"]}
	)

	game_id = payload.get("game_id")
	player_id_raw = payload.get("player_id")
	iat = payload.get("iat")
	exp = payload.get("exp")

	if not isinstance(game_id, str):
		raise ValueError("Invalid JWT payload: 'game_id' must be a string.")
	if not isinstance(player_id_raw, int):
		raise ValueError("Invalid JWT payload: 'player_id' must be an int.")
	if not isinstance(iat, int):
		raise ValueError("Invalid JWT payload: 'iat' must be an int.")
	if not isinstance(exp, int):
		raise ValueError("Invalid JWT payload: 'exp' must be an int.")

	player_id = PlayerId(player_id_raw)

	return {
		"game_id": game_id,
		"player_id": player_id,
		"iat": iat,
		"exp": exp,
	}
