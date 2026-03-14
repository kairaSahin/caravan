from enum import Enum


class MessageType(Enum):
	WELCOME = "welcome"
	STATE = "state"
	ERROR = "error"


class ErrorReason(Enum):
	LOBBY_FULL = "lobby_full"