import asyncio
import os
import uuid

from dotenv import load_dotenv
from realtime import BroadcastPayload, RealtimeSubscribeStates
from supabase import acreate_client

from game.player.enums import PlayerId
from game.setup.deck_builder import build_standard_deck
from game.setup.game_config import GameConfig
from game.setup.game_initializer import init_game
from numpy.random import default_rng

load_dotenv()


class GameHostDBBroadcast:
	def __init__(self, game_id: str, supabase_url: str, supabase_key: str) -> None:
		self.game_id = game_id
		self.supabase_url = supabase_url
		self.supabase_key = supabase_key

	async def run(self) -> None:
		game_config = GameConfig(
			deck_builder=build_standard_deck,
			starting_hand_size=8,
			starting_player=PlayerId.P1,
			shuffle_decks=True,
			random_generator=default_rng(),
		)

		state = init_game(game_config)

		print("[HOST] initial state created:", state.game_phase)

		supabase = await acreate_client(self.supabase_url, self.supabase_key)

		topic = f"game:{self.game_id}:moves"
		channel = supabase.channel(topic)

		def handle_move_broadcast(payload: BroadcastPayload) -> None:
			print("[HOST] broadcast received:", payload)

			inner = payload.get("payload")

			if inner:
				# TODO: Deserialize and run "step()" later
				print("[HOST] move payload:", inner.get("move"))

		def on_subscribe(status: RealtimeSubscribeStates, error: Exception | None) -> None:
			if error:
				print("[HOST] subscribe error:", error)
			else:
				print("[HOST] subscribed status:", status.value)

		await channel.on_broadcast(event="move_inserted", callback=handle_move_broadcast).subscribe(on_subscribe)

		print(f"[HOST] topic: {topic}")
		await asyncio.Future()


async def main() -> None:
	game_id = str(uuid.uuid4())
	supabase_url = os.environ["SUPABASE_URL"]
	supabase_key = os.environ["SUPABASE_KEY"]

	print("[host] GAME_ID:", game_id)

	host = GameHostDBBroadcast(game_id=game_id, supabase_url=supabase_url, supabase_key=supabase_key)
	await host.run()


if __name__ == "__main__":
	asyncio.run(main())
