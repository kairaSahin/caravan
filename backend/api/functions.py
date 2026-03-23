from postgrest.base_request_builder import SingleAPIResponse
from supabase import Client

from game.player.enums import PlayerId


def fetch_game_state_with_game_id_and_state_ver(game_id: str, state_version: int, supabase_client: Client) -> SingleAPIResponse:
	return (
		supabase_client.table("game_states")
		.select("*")
		.eq("game_id", game_id)
		.eq("state_version", state_version)
		.single()
		.execute()
	)


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


def fetch_player_hand_and_deck_size(player_state: dict) -> dict[str, int]:
	return {
		"deck_size": len(player_state["deck"]),
		"hand_size": len(player_state["hand"])
	}
