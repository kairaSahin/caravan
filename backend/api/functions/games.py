import os
import secrets
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import HTTPException
from postgrest import APIError
from postgrest.base_request_builder import SingleAPIResponse
from supabase import Client

from backend.api.auth.jwt_utils import create_game_player_token
from backend.api.enums import GameStatus, PlayerSlotStatus
from backend.api.errors import PostgresErrorCode, ErrorCode
from backend.api.schemas.games import GameRow, HostGameResponse
from game.player.enums import PlayerId

load_dotenv()

MAX_JOIN_CODE_ATTEMPTS = 20
# TODO: Might change ambiguity with I-1 and O-0
JOIN_CODE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
JOIN_CODE_LENGTH = 6


def generate_join_code():
	return "".join(secrets.choice(JOIN_CODE_ALPHABET) for _ in range(JOIN_CODE_LENGTH))


def insert_new_game(payload: dict, supabase_client: Client) -> SingleAPIResponse:
	result = (
		supabase_client.table("games")
		.insert(payload)
		.execute()
	)

	return result.data[0]


def host_game(supabase_client: Client) -> HostGameResponse:
	for _ in range(MAX_JOIN_CODE_ATTEMPTS):
		game_id = str(uuid4())
		join_code = generate_join_code()

		row = GameRow(
			game_id=game_id,
			join_code=join_code,
			status=GameStatus.WAITING_FOR_PLAYER,
			player_1_status=PlayerSlotStatus.JOINED,
			player_2_status=PlayerSlotStatus.EMPTY,
		)

		payload = row.model_dump(mode="json")

		try:
			result = insert_new_game(payload, supabase_client)
		except APIError as exc:
			exc_code = getattr(exc, "code", None)

			if exc_code == PostgresErrorCode.UNIQUE_CONSTRAINT_VIOLATION:
				continue

			else:
				raise HTTPException(
					status_code=500,
					detail={
						"code": ErrorCode.DB_ERROR,
						"message": f"Database error while creating lobby: {exc}",
					},
				)

		secret_key = os.environ["JWT_SECRET_KEY"]
		token = create_game_player_token(
			game_id=result["game_id"],
			player_id=PlayerId.P1,
			secret_key=secret_key
		)


		if result is not None:
			return HostGameResponse(
				game_id=result["game_id"],
				join_code=result["join_code"],
				token=token
			)

	raise HTTPException(
		status_code=500,
		detail={
			"code": ErrorCode.DB_ERROR,
			"message": "Failed to generate a unique join code",
		},
	)
