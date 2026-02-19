import asyncio
import os

import websockets
from dotenv import load_dotenv

load_dotenv()


# FIXME: Placeholder client code, to change.
async def main():
	port = int(os.environ.get("PORT"))

	uri = f"ws://127.0.0.1:{port}"

	async with websockets.connect(uri) as ws:
		await ws.send("Client connected")

		reply = await ws.recv()

		print("Client got:", reply)


if __name__ == "__main__":
	asyncio.run(main())
