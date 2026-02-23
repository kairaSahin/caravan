import asyncio
import json
import os

import websockets
from dotenv import load_dotenv
from websockets.legacy.client import WebSocketClientProtocol

from game.player.enums import PlayerId
from network.shared.deserializers import payload_to_game_state
from network.shared.enums import MessageType

load_dotenv()


class GameClient:
	def __init__(self, uri: str) -> None:
		self.uri = uri
		self.player_id: PlayerId | None = None

	async def run(self) -> None:
		async with websockets.connect(self.uri) as ws:
			await self._listen(ws)

	async def _listen(self, ws: WebSocketClientProtocol) -> None:
		print("Connected to host")

		async for raw in ws:
			message = json.loads(raw)
			await self._handle_message(message)

	async def _handle_message(self, message: dict) -> None:
		msg_type = message.get("type")

		if msg_type == MessageType.WELCOME.value:
			self.player_id = PlayerId(message["player_id"])
			print(f"Assigned player id: {self.player_id}")

		elif msg_type == MessageType.STATE.value:
			print("Received game state")
			print(message["state"])

			deserialized_game_state = payload_to_game_state(message["state"])

			print(f"Deserialized game state: \n{deserialized_game_state}")

		elif msg_type == MessageType.ERROR.value:
			print("Error:", message["reason"])

		else:
			print("Unknown message:", message)


async def main() -> None:
	port = int(os.environ.get("PORT"))
	uri = f"ws://127.0.0.1:{port}"

	client = GameClient(uri)
	await client.run()


if __name__ == "__main__":
	asyncio.run(main())
