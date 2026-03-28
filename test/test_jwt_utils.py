import jwt
import pytest
from datetime import timedelta, datetime, timezone

from backend.api.auth.jwt_utils import create_game_player_token, decode_game_player_token
from game.player.enums import PlayerId


def test_jwt_roundtrip_game_and_player_ids() -> None:
	secret = "test-secret-key-that-is-at-least-32-bytes"
	game_id = "game-123"
	player_id = PlayerId.P2

	token = create_game_player_token(game_id=game_id, player_id=player_id, secret_key=secret)
	payload = decode_game_player_token(token=token, secret_key=secret)

	assert payload["game_id"] == game_id
	assert payload["player_id"] == player_id
	assert isinstance(payload["iat"], int)
	assert isinstance(payload["exp"], int)
	assert payload["exp"] > payload["iat"]


def test_jwt_decode_rejects_invalid_payload_shape() -> None:
	secret = "test-secret-key-that-is-at-least-32-bytes"
	now = int(datetime.now(timezone.utc).timestamp())
	token = jwt.encode(
		{"game_id": 123, "player_id": "2", "iat": now, "exp": now + 3600},
		secret,
		algorithm="HS256",
	)

	with pytest.raises(ValueError):
		decode_game_player_token(token=token, secret_key=secret)


def test_jwt_decode_rejects_expired_token() -> None:
	secret = "test-secret-key-that-is-at-least-32-bytes"
	game_id = "game-123"
	player_id = PlayerId.P1

	token = create_game_player_token(
		game_id=game_id,
		player_id=player_id,
		secret_key=secret,
		expires_in=timedelta(seconds=-1),
	)

	with pytest.raises(jwt.ExpiredSignatureError):
		decode_game_player_token(token=token, secret_key=secret)


def test_jwt_decode_rejects_missing_required_claims() -> None:
	secret = "test-secret-key-that-is-at-least-32-bytes"
	token = jwt.encode({"game_id": "game-123", "player_id": int(PlayerId.P1)}, secret, algorithm="HS256")

	with pytest.raises(jwt.InvalidTokenError):
		decode_game_player_token(token=token, secret_key=secret)
