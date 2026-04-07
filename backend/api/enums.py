from enum import StrEnum


class GameStatus(StrEnum):
	WAITING_FOR_PLAYER = "waiting_for_player"
	READY = "ready"
	STARTED = "started"
	FINISHED = "finished"
	ABANDONED = "abandoned"


class PlayerSlotStatus(StrEnum):
	EMPTY = "empty"
	JOINED = "joined"
	DISCONNECTED = "disconnected"


class DeckType(StrEnum):
	STANDARD = "standard"
	CUSTOM = "custom"