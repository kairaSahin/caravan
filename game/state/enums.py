from enum import IntEnum, Enum


class GamePhase(IntEnum):
	SETUP = 0
	MAIN = 1
	FINISHED = 2


class WinReason(Enum):
	TWO_CARAVANS = "two_caravans"
	THREE_CARAVANS = "three_caravans"
	CONCEDE = "concede"
	OUT_OF_CARDS = "out_of_cards"
