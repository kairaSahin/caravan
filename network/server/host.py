import asyncio
import os
import websockets

from websockets.legacy.server import WebSocketServerProtocol
from game.player.enums import PlayerId
from game.setup.deck_builder import build_standard_deck
from game.setup.game_config import GameConfig
from game.setup.game_initializer import init_game
from game.state.game_state import GameState
from numpy.random import default_rng
from dotenv import load_dotenv

load_dotenv()


# FIXME: Placeholder host code, to change.
class GameHost:
	def __init__(self, state: GameState, host: str, port: int) -> None:
		self.state = state
		self.host = host
		self.port = port

	async def handler(self, ws: WebSocketServerProtocol) -> None:
		print("Host connected")

		try:
			async for message in ws:
				print(f"Message received: {message}")

				await ws.send(str(self.state.game_phase.get_name))

		except websockets.ConnectionClosed:
			print("Connection closed")


async def main() -> None:
	game_config = GameConfig(
		deck_builder=build_standard_deck,
		starting_hand_size=8,
		starting_player=PlayerId.P1,
		shuffle_decks=True,
		random_generator=default_rng(42)
	)

	state = init_game(game_config)
	host = os.environ.get("HOST")
	port = int(os.environ.get("PORT"))

	game_host = GameHost(state=state, host=host, port=port)

	async with websockets.serve(handler=game_host.handler, host=game_host.host, port=game_host.port):
		print(f"Listening on ws://{game_host.host}:{game_host.port}")
		await asyncio.Future()


if __name__ == "__main__":
	asyncio.run(main())
