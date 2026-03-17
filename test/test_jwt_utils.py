import jwt
import pytest

from backend.api.auth.jwt_utils import create_game_player_token, decode_game_player_token
from game.player.enums import PlayerId


def test_jwt_roundtrip_game_and_player_ids() -> None:
	secret = "test-secret"
	game_id = "game-123"
	player_id = PlayerId.P2

	token = create_game_player_token(game_id=game_id, player_id=player_id, secret_key=secret)
	payload = decode_game_player_token(token=token, secret_key=secret)

	assert payload["game_id"] == game_id
	assert payload["player_id"] == player_id


def test_jwt_decode_rejects_invalid_payload_shape() -> None:
	secret = "test-secret"
	token = jwt.encode({"game_id": 123, "player_id": "2"}, secret, algorithm="HS256")

	with pytest.raises(ValueError):
		decode_game_player_token(token=token, secret_key=secret)
