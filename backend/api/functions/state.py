from typing import Any

from fastapi import HTTPException
from postgrest import APIError
from postgrest.base_request_builder import SingleAPIResponse
from supabase import Client

from backend.api.errors import ErrorCode
from backend.shared.serializers import game_state_to_payload
from game.player.enums import PlayerId
from game.state.game_state import GameState


def fetch_latest_game_state_with_game_id(game_id: str, supabase_client: Client) -> SingleAPIResponse:
	return (
		supabase_client.table("game_states")
		.select("*")
		.eq("game_id", game_id)
		.order("state_version", desc=True)
		.limit(1)
		.single()
		.execute()
	)


def insert_game_state(game_id: str, current_state_version: int, state: GameState,
					  supabase_client: Client) -> SingleAPIResponse:
	serialized_game_state = game_state_to_payload(state)

	result = (
		supabase_client.table("game_states")
		.insert({"game_id": game_id, "state_version": current_state_version + 1, "state": serialized_game_state})
		.execute()
	)

	return result.data[0]


def game_state_to_player_exclusive_state(game_state_payload: dict,
										 player_id: PlayerId) -> dict:
	players = game_state_payload.pop("players", None)

	if players is None:
		raise ValueError("No players found in fetched game state.")

	players_by_id = {PlayerId(int(k)): v for k, v in players.items()}

	player = players_by_id[player_id]
	opponent_id = PlayerId.P1 if player_id == PlayerId.P2 else PlayerId.P2
	opponent = fetch_player_hand_and_deck_size(players_by_id[opponent_id])

	return {
		**game_state_payload,
		"player": player,
		"opponent": opponent
	}


def handle_state_fetch(
		game_id: str,
		player_id: PlayerId | None,
		is_player_exclusive: bool,
		supabase_client: Client) -> tuple[Any, Any, dict]:
	try:
		result = fetch_latest_game_state_with_game_id(game_id, supabase_client)

		row = result.data

		if row is None:
			raise HTTPException(status_code=404, detail="Game state not found")

		state_payload = row["state"]

		if is_player_exclusive and player_id is not None:
			state_payload = game_state_to_player_exclusive_state(state_payload, player_id)

		db_game_id = row["game_id"]
		db_version = row["state_version"]


	except HTTPException as exc:
		raise exc
	except APIError as exc:
		raise HTTPException(
			status_code=500,
			detail={
				"code": ErrorCode.DB_ERROR,
				"message": f"Database error while processing state: {exc}",
			},
		)
	except KeyError as exc:
		raise HTTPException(
			status_code=500,
			detail={
				"code": ErrorCode.MALFORMED_STATE,
				"message": f"Malformed game state payload: missing key {exc.args[0]}"
			}
		)
	except Exception as exc:
		raise HTTPException(
			status_code=500,
			detail={
				"code": ErrorCode.UNEXPECTED_ERROR,
				"message": f"Unexpected error while building state response: {exc}"
			}
		)

	return db_game_id, db_version, state_payload


def fetch_player_hand_and_deck_size(player_state: dict) -> dict[str, int]:
	return {
		"deck_size": len(player_state["deck"]),
		"hand_size": len(player_state["hand"])
	}
