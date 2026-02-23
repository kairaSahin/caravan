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

from network.server.functions import create_dumped_message
from network.shared.enums import MessageType, ErrorReason
from network.shared.serializers import game_state_to_payload

load_dotenv()


class GameHost:
	def __init__(self, state: GameState, host: str, port: int) -> None:
		self.state = state
		self.host = host
		self.port = port
		self.connections: dict[WebSocketServerProtocol, PlayerId] = {}

	def _assign_player_id(self) -> PlayerId | None:
		taken = set(self.connections.values())

		if PlayerId.P1 not in taken:
			return PlayerId.P1
		if PlayerId.P2 not in taken:
			return PlayerId.P2

		return None

	async def run(self) -> None:
		async with websockets.serve(
				handler=self.handler,
				host=self.host,
				port=self.port
		):
			print(f"Listening on ws://{self.host}:{self.port}")
			await asyncio.Future()

	async def handler(self, ws: WebSocketServerProtocol) -> None:
		print("Client connected")

		player_id = self._assign_player_id()

		if player_id is None:
			await ws.send(create_dumped_message(MessageType.ERROR, {"reason": ErrorReason.LOBBY_FULL.value}))
			await ws.close()
			return

		self.connections[ws] = player_id

		await ws.send(create_dumped_message(MessageType.WELCOME, {"player_id": player_id.value}))

		await ws.send(create_dumped_message(MessageType.STATE, {"state": game_state_to_payload(self.state)}))

		try:
			async for message in ws:
				print(f"Message received from {player_id}: {message}")

		except websockets.ConnectionClosed:
			print("Connection closed")

		finally:
			del self.connections[ws]


async def main() -> None:
	game_config = GameConfig(
		deck_builder=build_standard_deck,
		starting_hand_size=8,
		starting_player=PlayerId.P1,
		shuffle_decks=True,
		random_generator=default_rng()
	)

	state = init_game(game_config)
	host = os.environ.get("HOST")
	port = int(os.environ.get("PORT"))

	game_host = GameHost(state=state, host=host, port=port)

	await game_host.run()


if __name__ == "__main__":
	asyncio.run(main())
